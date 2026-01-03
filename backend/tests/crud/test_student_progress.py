"""Tests for StudentProgress CRUD operations."""

import uuid

from sqlmodel import Session

from app import crud
from app.models import StudentProgressCreate, StudentProgressUpdate
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def test_create_student_progress(db: Session) -> None:
    """Test creating student progress."""
    user = create_random_user(db)
    module_name = random_lower_string()
    progress_in = StudentProgressCreate(
        module_name=module_name,
        progress=50,
        struggling=False,
        last_score=55.5,
        attempts=1,
    )
    progress = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    assert progress.module_name == module_name
    assert progress.progress == 50
    assert progress.struggling is False
    assert progress.last_score == 55.5
    assert progress.attempts == 1
    assert progress.user_id == user.id


def test_get_student_progress_for_user(db: Session) -> None:
    """Test retrieving all progress for a user."""
    user = create_random_user(db)
    
    # Create multiple progress entries
    for i in range(3):
        progress_in = StudentProgressCreate(
            module_name=f"module_{i}",
            progress=30 + i * 10,
            struggling=i == 0,
            attempts=i + 1,
        )
        crud.create_or_update_student_progress(
            session=db, user_id=user.id, progress_in=progress_in
        )
    
    all_progress = crud.get_student_progress_for_user(session=db, user_id=user.id)
    assert len(all_progress) >= 3


def test_get_student_progress_by_module(db: Session) -> None:
    """Test retrieving progress for a specific module."""
    user = create_random_user(db)
    module_name = random_lower_string()
    progress_in = StudentProgressCreate(
        module_name=module_name,
        progress=75,
        struggling=False,
        attempts=2,
    )
    created = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    retrieved = crud.get_student_progress_by_module(
        session=db, user_id=user.id, module_name=module_name
    )
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.module_name == module_name


def test_update_student_progress(db: Session) -> None:
    """Test updating existing student progress."""
    user = create_random_user(db)
    module_name = random_lower_string()
    
    # Create initial progress
    progress_in = StudentProgressCreate(
        module_name=module_name,
        progress=40,
        struggling=True,
        last_score=35.0,
        attempts=1,
    )
    initial = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    # Update progress
    progress_update = StudentProgressCreate(
        module_name=module_name,
        progress=80,
        struggling=False,
        last_score=85.0,
        attempts=2,
    )
    updated = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_update
    )
    
    # Should be the same record, just updated
    assert updated.id == initial.id
    assert updated.progress == 80
    assert updated.struggling is False
    assert updated.last_score == 85.0
    assert updated.attempts == 2


def test_set_student_progress_fields(db: Session) -> None:
    """Test setting specific fields on student progress."""
    user = create_random_user(db)
    module_name = random_lower_string()
    
    # Create initial progress
    progress_in = StudentProgressCreate(
        module_name=module_name,
        progress=50,
        struggling=False,
        attempts=1,
    )
    progress = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    # Update only specific fields
    partial_update = StudentProgressUpdate(progress=70, struggling=True)
    updated = crud.set_student_progress_fields(
        session=db, progress_obj=progress, progress_update=partial_update
    )
    
    assert updated.id == progress.id
    assert updated.progress == 70
    assert updated.struggling is True
    assert updated.module_name == module_name  # Unchanged
    assert updated.attempts == 1  # Unchanged


def test_get_struggling_modules_for_user(db: Session) -> None:
    """Test retrieving struggling modules."""
    user = create_random_user(db)
    
    # Create progress entries with different statuses
    struggling_module = StudentProgressCreate(
        module_name="struggling_module",
        progress=80,
        struggling=True,  # Marked as struggling
        attempts=5,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=struggling_module
    )
    
    low_progress_module = StudentProgressCreate(
        module_name="low_progress_module",
        progress=45,  # Below default threshold of 60
        struggling=False,
        attempts=2,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=low_progress_module
    )
    
    good_module = StudentProgressCreate(
        module_name="good_module",
        progress=90,
        struggling=False,
        attempts=1,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=good_module
    )
    
    # Get struggling modules with default threshold (60)
    struggling = crud.get_struggling_modules_for_user(
        session=db, user_id=user.id, progress_threshold=60
    )
    
    # Should include struggling_module and low_progress_module but not good_module
    assert len(struggling) >= 2
    module_names = {m.module_name for m in struggling}
    assert "struggling_module" in module_names
    assert "low_progress_module" in module_names
    assert "good_module" not in module_names


def test_get_struggling_modules_custom_threshold(db: Session) -> None:
    """Test struggling modules with custom threshold."""
    user = create_random_user(db)
    
    progress_in = StudentProgressCreate(
        module_name="module_at_70",
        progress=70,
        struggling=False,
        attempts=1,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    # With threshold 60, should not be struggling
    struggling_60 = crud.get_struggling_modules_for_user(
        session=db, user_id=user.id, progress_threshold=60
    )
    module_names_60 = {m.module_name for m in struggling_60}
    assert "module_at_70" not in module_names_60
    
    # With threshold 80, should be struggling
    struggling_80 = crud.get_struggling_modules_for_user(
        session=db, user_id=user.id, progress_threshold=80
    )
    module_names_80 = {m.module_name for m in struggling_80}
    assert "module_at_70" in module_names_80


def test_student_progress_user_isolation(db: Session) -> None:
    """Test that progress is isolated between users."""
    user1 = create_random_user(db)
    user2 = create_random_user(db)
    
    module_name = "shared_module"
    
    # Create progress for user1
    progress_in = StudentProgressCreate(
        module_name=module_name,
        progress=50,
        struggling=False,
        attempts=1,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user1.id, progress_in=progress_in
    )
    
    # Check user2 doesn't see user1's progress
    user2_progress = crud.get_student_progress_by_module(
        session=db, user_id=user2.id, module_name=module_name
    )
    assert user2_progress is None
    
    # Create progress for user2
    crud.create_or_update_student_progress(
        session=db, user_id=user2.id, progress_in=progress_in
    )
    
    # Each user should have their own progress
    user1_all = crud.get_student_progress_for_user(session=db, user_id=user1.id)
    user2_all = crud.get_student_progress_for_user(session=db, user_id=user2.id)
    
    # Both should have progress records
    assert len(user1_all) >= 1
    assert len(user2_all) >= 1
    
    # But the records should be different
    user1_ids = {p.id for p in user1_all}
    user2_ids = {p.id for p in user2_all}
    assert user1_ids.isdisjoint(user2_ids)
