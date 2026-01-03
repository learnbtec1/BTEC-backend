"""Tests for StudentProgress CRUD operations."""

from sqlmodel import Session

from app import crud
from app.models import StudentProgressCreate, StudentProgressUpdate, UserCreate
from tests.utils.utils import random_email, random_lower_string


def test_create_student_progress(db: Session) -> None:
    """Test creating a student progress record."""
    # Create a user first
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create student progress
    progress_in = StudentProgressCreate(
        module_name="Python Basics",
        progress_percentage=75,
        struggling=False,
        last_activity="Completed quiz 3",
    )
    progress = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )

    assert progress.module_name == "Python Basics"
    assert progress.progress_percentage == 75
    assert progress.struggling is False
    assert progress.last_activity == "Completed quiz 3"
    assert progress.user_id == user.id


def test_update_student_progress(db: Session) -> None:
    """Test updating an existing student progress record."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create initial progress
    progress_in = StudentProgressCreate(
        module_name="Data Structures",
        progress_percentage=30,
        struggling=True,
    )
    progress = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    assert progress.progress_percentage == 30

    # Update the progress
    progress_update = StudentProgressCreate(
        module_name="Data Structures",
        progress_percentage=60,
        struggling=False,
        last_activity="Finished assignment",
    )
    updated_progress = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_update
    )

    assert updated_progress.id == progress.id  # Same record
    assert updated_progress.progress_percentage == 60
    assert updated_progress.struggling is False
    assert updated_progress.last_activity == "Finished assignment"


def test_get_student_progress_for_user(db: Session) -> None:
    """Test retrieving all progress records for a user."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create multiple progress records
    modules = ["Module A", "Module B", "Module C"]
    for module in modules:
        progress_in = StudentProgressCreate(
            module_name=module, progress_percentage=50, struggling=False
        )
        crud.create_or_update_student_progress(
            session=db, user_id=user.id, progress_in=progress_in
        )

    # Retrieve all progress
    all_progress = crud.get_student_progress_for_user(session=db, user_id=user.id)
    assert len(all_progress) == 3
    module_names = {p.module_name for p in all_progress}
    assert module_names == set(modules)


def test_get_student_progress_by_module(db: Session) -> None:
    """Test retrieving progress for a specific module."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create progress for a specific module
    progress_in = StudentProgressCreate(
        module_name="Advanced Python", progress_percentage=85, struggling=False
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )

    # Retrieve by module
    progress = crud.get_student_progress_by_module(
        session=db, user_id=user.id, module_name="Advanced Python"
    )
    assert progress is not None
    assert progress.module_name == "Advanced Python"
    assert progress.progress_percentage == 85

    # Try non-existent module
    non_existent = crud.get_student_progress_by_module(
        session=db, user_id=user.id, module_name="Non-Existent Module"
    )
    assert non_existent is None


def test_set_student_progress_fields(db: Session) -> None:
    """Test updating specific fields of a progress record."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create progress
    progress_in = StudentProgressCreate(
        module_name="Algorithms", progress_percentage=40, struggling=True
    )
    progress = crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )

    # Update only specific fields
    update = StudentProgressUpdate(
        progress_percentage=70, last_activity="Completed project"
    )
    updated = crud.set_student_progress_fields(
        session=db, progress_obj=progress, progress_update=update
    )

    assert updated.progress_percentage == 70
    assert updated.last_activity == "Completed project"
    assert updated.struggling is True  # Unchanged
    assert updated.module_name == "Algorithms"  # Unchanged


def test_get_struggling_modules_for_user(db: Session) -> None:
    """Test retrieving modules where student is struggling."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create progress records with varying levels
    test_data = [
        ("Module 1", 90, False),  # Good progress, not struggling
        ("Module 2", 50, False),  # Below threshold
        ("Module 3", 70, True),  # Above threshold but marked struggling
        ("Module 4", 30, True),  # Below threshold and struggling
        ("Module 5", 80, False),  # Good progress, not struggling
    ]

    for module_name, percentage, struggling in test_data:
        progress_in = StudentProgressCreate(
            module_name=module_name,
            progress_percentage=percentage,
            struggling=struggling,
        )
        crud.create_or_update_student_progress(
            session=db, user_id=user.id, progress_in=progress_in
        )

    # Get struggling modules with default threshold (60)
    struggling = crud.get_struggling_modules_for_user(session=db, user_id=user.id)
    assert len(struggling) == 3
    struggling_names = {p.module_name for p in struggling}
    assert struggling_names == {"Module 2", "Module 3", "Module 4"}

    # Test with different threshold
    struggling_40 = crud.get_struggling_modules_for_user(
        session=db, user_id=user.id, progress_threshold=40
    )
    assert len(struggling_40) == 2
    struggling_40_names = {p.module_name for p in struggling_40}
    assert struggling_40_names == {"Module 3", "Module 4"}
