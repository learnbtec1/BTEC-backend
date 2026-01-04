"""Tests for virtual tutor recommendation logic."""

from sqlmodel import Session

from app import crud
from app.models import StudentProgressCreate
from app.virtual_tutor import recommend_remediation
from tests.utils.user import create_random_user


def test_recommend_remediation_no_struggling_modules(db: Session) -> None:
    """Test recommendations when user has no struggling modules."""
    user = create_random_user(db)
    
    # Create progress with good scores
    for i in range(3):
        progress_in = StudentProgressCreate(
            module_name=f"module_{i}",
            progress=80 + i * 5,
            struggling=False,
            last_score=85.0,
            attempts=1,
        )
        crud.create_or_update_student_progress(
            session=db, user_id=user.id, progress_in=progress_in
        )
    
    recommendations = recommend_remediation(session=db, user=user, threshold=60)
    assert len(recommendations) == 0


def test_recommend_remediation_with_struggling_modules(db: Session) -> None:
    """Test recommendations when user has struggling modules."""
    user = create_random_user(db)
    
    # Create struggling module
    struggling = StudentProgressCreate(
        module_name="difficult_module",
        progress=40,
        struggling=True,
        last_score=35.0,
        attempts=3,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=struggling
    )
    
    # Create low progress module
    low_progress = StudentProgressCreate(
        module_name="challenging_module",
        progress=55,
        struggling=False,
        last_score=50.0,
        attempts=2,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=low_progress
    )
    
    recommendations = recommend_remediation(session=db, user=user, threshold=60)
    assert len(recommendations) == 2
    
    # Check structure of recommendations
    for rec in recommendations:
        assert "module_name" in rec
        assert "current_progress" in rec
        assert "last_score" in rec
        assert "attempts" in rec
        assert "struggling" in rec
        assert "recommended_action" in rec
        assert "resources" in rec


def test_recommend_remediation_content_low_progress(db: Session) -> None:
    """Test recommendation content for very low progress."""
    user = create_random_user(db)
    
    progress_in = StudentProgressCreate(
        module_name="fundamentals",
        progress=25,
        struggling=True,
        last_score=20.0,
        attempts=1,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    recommendations = recommend_remediation(session=db, user=user)
    assert len(recommendations) == 1
    
    rec = recommendations[0]
    assert rec["module_name"] == "fundamentals"
    assert rec["current_progress"] == 25
    assert rec["last_score"] == 20.0
    assert "fundamental" in rec["recommended_action"].lower()
    assert len(rec["resources"]) > 0


def test_recommend_remediation_content_medium_progress(db: Session) -> None:
    """Test recommendation content for medium progress."""
    user = create_random_user(db)
    
    progress_in = StudentProgressCreate(
        module_name="intermediate_topic",
        progress=55,
        struggling=False,
        last_score=52.0,
        attempts=2,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    recommendations = recommend_remediation(session=db, user=user)
    assert len(recommendations) == 1
    
    rec = recommendations[0]
    assert rec["current_progress"] == 55
    assert rec["last_score"] == 52.0
    assert rec["attempts"] == 2
    assert len(rec["resources"]) > 0


def test_recommend_remediation_high_attempts(db: Session) -> None:
    """Test recommendations include tutoring for high attempt counts."""
    user = create_random_user(db)
    
    progress_in = StudentProgressCreate(
        module_name="difficult_module",
        progress=50,
        struggling=True,
        last_score=45.0,
        attempts=5,  # High attempts
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    recommendations = recommend_remediation(session=db, user=user)
    assert len(recommendations) == 1
    
    rec = recommendations[0]
    assert rec["attempts"] == 5
    # Should recommend tutoring for high attempts
    resources_text = " ".join(rec["resources"]).lower()
    assert "tutor" in resources_text


def test_recommend_remediation_low_score_resources(db: Session) -> None:
    """Test that low scores trigger appropriate resource recommendations."""
    user = create_random_user(db)
    
    progress_in = StudentProgressCreate(
        module_name="struggling_topic",
        progress=55,
        struggling=False,
        last_score=40.0,  # Low score
        attempts=2,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    recommendations = recommend_remediation(session=db, user=user)
    assert len(recommendations) == 1
    
    rec = recommendations[0]
    assert rec["last_score"] == 40.0
    # Should include video tutorials and practice problems
    resources_text = " ".join(rec["resources"]).lower()
    assert any(keyword in resources_text for keyword in ["video", "practice"])


def test_recommend_remediation_custom_threshold(db: Session) -> None:
    """Test recommendations with custom threshold."""
    user = create_random_user(db)
    
    # Create module with 70% progress
    progress_in = StudentProgressCreate(
        module_name="module_70",
        progress=70,
        struggling=False,
        attempts=1,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    # With default threshold 60, should not appear
    recs_60 = recommend_remediation(session=db, user=user, threshold=60)
    module_names_60 = {r["module_name"] for r in recs_60}
    assert "module_70" not in module_names_60
    
    # With threshold 80, should appear
    recs_80 = recommend_remediation(session=db, user=user, threshold=80)
    module_names_80 = {r["module_name"] for r in recs_80}
    assert "module_70" in module_names_80


def test_recommend_remediation_struggling_flag_overrides_progress(db: Session) -> None:
    """Test that struggling flag shows module even if progress is high."""
    user = create_random_user(db)
    
    # High progress but marked as struggling
    progress_in = StudentProgressCreate(
        module_name="confusing_module",
        progress=85,  # High progress
        struggling=True,  # But marked as struggling
        last_score=90.0,
        attempts=4,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    recommendations = recommend_remediation(session=db, user=user, threshold=60)
    assert len(recommendations) == 1
    assert recommendations[0]["module_name"] == "confusing_module"
    assert recommendations[0]["struggling"] is True


def test_recommend_remediation_multiple_modules_sorted(db: Session) -> None:
    """Test recommendations with multiple modules."""
    user = create_random_user(db)
    
    modules = [
        ("module_a", 30, True, 25.0, 5),
        ("module_b", 55, False, 50.0, 2),
        ("module_c", 45, True, 40.0, 3),
    ]
    
    for name, progress, struggling, score, attempts in modules:
        progress_in = StudentProgressCreate(
            module_name=name,
            progress=progress,
            struggling=struggling,
            last_score=score,
            attempts=attempts,
        )
        crud.create_or_update_student_progress(
            session=db, user_id=user.id, progress_in=progress_in
        )
    
    recommendations = recommend_remediation(session=db, user=user)
    assert len(recommendations) == 3
    
    # Verify all modules are included
    module_names = {r["module_name"] for r in recommendations}
    assert module_names == {"module_a", "module_b", "module_c"}


def test_recommend_remediation_resources_not_empty(db: Session) -> None:
    """Test that all recommendations include at least one resource."""
    user = create_random_user(db)
    
    # Create various types of struggling modules
    modules = [
        ("very_low", 20, True, 15.0, 1),
        ("low", 40, False, 35.0, 2),
        ("medium", 55, True, 50.0, 3),
        ("approaching", 68, False, 65.0, 1),
    ]
    
    for name, progress, struggling, score, attempts in modules:
        progress_in = StudentProgressCreate(
            module_name=name,
            progress=progress,
            struggling=struggling,
            last_score=score,
            attempts=attempts,
        )
        crud.create_or_update_student_progress(
            session=db, user_id=user.id, progress_in=progress_in
        )
    
    recommendations = recommend_remediation(session=db, user=user)
    
    # Every recommendation should have at least one resource
    for rec in recommendations:
        assert len(rec["resources"]) > 0
        # Resources should be strings
        for resource in rec["resources"]:
            assert isinstance(resource, str)
            assert len(resource) > 0
