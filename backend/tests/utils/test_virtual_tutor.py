"""Tests for virtual tutor recommendation logic."""

from sqlmodel import Session

from app import crud
from app.models import StudentProgressCreate, UserCreate
from app.virtual_tutor import recommend_remediation
from tests.utils.utils import random_email, random_lower_string


def test_recommend_remediation_no_struggling_modules(db: Session) -> None:
    """Test that no recommendations are returned when student is doing well."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create progress with good performance
    progress_in = StudentProgressCreate(
        module_name="Advanced Topics", progress_percentage=85, struggling=False
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )

    # Get recommendations
    recommendations = recommend_remediation(session=db, user=user)
    assert len(recommendations) == 0


def test_recommend_remediation_with_struggling_modules(db: Session) -> None:
    """Test recommendations for struggling students."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create progress records with struggling modules
    test_data = [
        ("Python Basics", 25, True),  # Very low progress
        ("Data Structures", 50, False),  # Medium low progress
        ("Algorithms", 80, False),  # Good progress, should not be in recommendations
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

    # Get recommendations
    recommendations = recommend_remediation(session=db, user=user, threshold=60)

    # Should have 2 recommendations
    assert len(recommendations) == 2

    # Check that recommendations have expected structure
    for rec in recommendations:
        assert "module_name" in rec
        assert "current_progress" in rec
        assert "struggling" in rec
        assert "recommendations" in rec
        assert isinstance(rec["recommendations"], list)
        assert len(rec["recommendations"]) > 0

    # Check specific modules
    module_names = {r["module_name"] for r in recommendations}
    assert "Python Basics" in module_names
    assert "Data Structures" in module_names
    assert "Algorithms" not in module_names


def test_recommend_remediation_low_progress(db: Session) -> None:
    """Test recommendations for very low progress (<30%)."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create progress with very low performance
    progress_in = StudentProgressCreate(
        module_name="Introduction to Programming",
        progress_percentage=20,
        struggling=True,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )

    # Get recommendations
    recommendations = recommend_remediation(session=db, user=user)

    assert len(recommendations) == 1
    rec = recommendations[0]
    assert rec["module_name"] == "Introduction to Programming"
    assert rec["current_progress"] == 20

    # Check that recommendations are appropriate for low progress
    rec_text = " ".join(rec["recommendations"])
    assert "fundamental" in rec_text.lower() or "introductory" in rec_text.lower()


def test_recommend_remediation_medium_progress(db: Session) -> None:
    """Test recommendations for medium progress (30-59%)."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create progress with medium performance
    progress_in = StudentProgressCreate(
        module_name="Web Development", progress_percentage=45, struggling=False
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )

    # Get recommendations
    recommendations = recommend_remediation(session=db, user=user)

    assert len(recommendations) == 1
    rec = recommendations[0]
    assert rec["module_name"] == "Web Development"
    assert rec["current_progress"] == 45

    # Check that recommendations are appropriate for medium progress
    rec_text = " ".join(rec["recommendations"])
    assert "intermediate" in rec_text.lower() or "practice" in rec_text.lower()


def test_recommend_remediation_custom_threshold(db: Session) -> None:
    """Test recommendations with custom threshold."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create multiple progress records
    test_data = [
        ("Module A", 40, False),
        ("Module B", 60, False),
        ("Module C", 75, False),
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

    # Get recommendations with threshold of 50
    recommendations = recommend_remediation(session=db, user=user, threshold=50)
    assert len(recommendations) == 1
    assert recommendations[0]["module_name"] == "Module A"

    # Get recommendations with threshold of 70
    recommendations_70 = recommend_remediation(session=db, user=user, threshold=70)
    assert len(recommendations_70) == 2
    module_names = {r["module_name"] for r in recommendations_70}
    assert module_names == {"Module A", "Module B"}


def test_recommend_remediation_includes_ar(db: Session) -> None:
    """Test that recommendations include AR-related suggestions."""
    # Create a user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create progress with struggling module
    progress_in = StudentProgressCreate(
        module_name="3D Modeling", progress_percentage=35, struggling=True
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )

    # Get recommendations
    recommendations = recommend_remediation(session=db, user=user)

    assert len(recommendations) == 1
    rec = recommendations[0]

    # Check that AR recommendations are present
    rec_text = " ".join(rec["recommendations"])
    assert "AR" in rec_text or "3D" in rec_text
