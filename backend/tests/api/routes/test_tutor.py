"""Tests for tutor API endpoints."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.models import StudentProgressCreate, UserCreate
from tests.utils.utils import random_email, random_lower_string


def test_get_tutor_recommendations_authenticated(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Test getting recommendations as an authenticated user."""
    # Get the current user from the token
    email = settings.EMAIL_TEST_USER
    user = crud.get_user_by_email(session=db, email=email)
    assert user is not None

    # Create some progress data for the user
    progress_data = [
        ("Python Basics", 40, True),
        ("Advanced Python", 80, False),
    ]

    for module_name, percentage, struggling in progress_data:
        progress_in = StudentProgressCreate(
            module_name=module_name,
            progress_percentage=percentage,
            struggling=struggling,
        )
        crud.create_or_update_student_progress(
            session=db, user_id=user.id, progress_in=progress_in
        )

    # Call the endpoint
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "user_id" in data
    assert "user_email" in data
    assert "threshold" in data
    assert "recommendations" in data
    assert data["user_email"] == email
    assert data["threshold"] == 60  # Default threshold

    # Should have one recommendation (Python Basics)
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["module_name"] == "Python Basics"


def test_get_tutor_recommendations_with_custom_threshold(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Test getting recommendations with custom threshold."""
    # Get the current user from the token
    email = settings.EMAIL_TEST_USER
    user = crud.get_user_by_email(session=db, email=email)
    assert user is not None

    # Create progress data
    progress_data = [
        ("Module A", 30, False),
        ("Module B", 50, False),
        ("Module C", 75, False),
    ]

    for module_name, percentage, struggling in progress_data:
        progress_in = StudentProgressCreate(
            module_name=module_name,
            progress_percentage=percentage,
            struggling=struggling,
        )
        crud.create_or_update_student_progress(
            session=db, user_id=user.id, progress_in=progress_in
        )

    # Call with threshold of 40
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=40",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["threshold"] == 40
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["module_name"] == "Module A"

    # Call with threshold of 70
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=70",
        headers=normal_user_token_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["threshold"] == 70
    assert len(data["recommendations"]) == 2


def test_get_tutor_recommendations_no_progress(client: TestClient, db: Session) -> None:
    """Test getting recommendations for a new user with no progress data."""
    # Create a new user
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.create_user(session=db, user_create=user_in)

    # Create token for the new user
    from app.core.security import create_access_token

    access_token = create_access_token(subject=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    # Call the endpoint
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations", headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["user_email"] == email
    assert len(data["recommendations"]) == 0


def test_get_tutor_recommendations_unauthenticated(client: TestClient) -> None:
    """Test that unauthenticated requests are rejected."""
    response = client.get(f"{settings.API_V1_STR}/tutor/recommendations")
    assert response.status_code == 401


def test_get_tutor_recommendations_invalid_threshold(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test that invalid threshold values are handled properly."""
    # Threshold too low
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=-10",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 422  # Validation error

    # Threshold too high
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=150",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 422  # Validation error
