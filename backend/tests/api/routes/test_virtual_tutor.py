from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.core.security import create_access_token
from app.models import StudentProgressCreate
from tests.utils.user import create_random_user
from tests.utils.utils import get_superuser_token_headers


def test_get_virtual_tutor_recommendations_authenticated(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Test getting recommendations with authenticated user."""
    response = client.get(
        f"{settings.API_V1_STR}/virtual-tutor/recommendations",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "analysis" in content
    assert "study_recommendations" in content
    assert "ar_simulations" in content
    assert "motivational_feedback" in content


def test_get_virtual_tutor_recommendations_no_progress(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Test recommendations for user with no progress data."""
    response = client.get(
        f"{settings.API_V1_STR}/virtual-tutor/recommendations",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    
    # Should have empty analysis
    assert content["analysis"]["total_topics"] == 0
    assert content["analysis"]["overall_score"] == 0.0
    assert len(content["analysis"]["weak_areas"]) == 0
    assert len(content["study_recommendations"]) == 0


def test_get_virtual_tutor_recommendations_with_progress(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Test recommendations with actual progress data."""
    # Create a test user with progress
    user = create_random_user(db)
    
    # Add some progress entries - mix of good and weak areas
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Science", topic="Biology", score=45.0, completed=True
        ),
        student_id=user.id,
    )
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Mathematics", topic="Calculus", score=85.0, completed=True
        ),
        student_id=user.id,
    )
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Physics", topic="Mechanics", score=50.0, completed=False
        ),
        student_id=user.id,
    )
    
    # Get token for this user
    token = create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(
        f"{settings.API_V1_STR}/virtual-tutor/recommendations",
        headers=headers,
    )
    assert response.status_code == 200
    content = response.json()
    
    # Verify analysis
    assert content["analysis"]["total_topics"] == 3
    assert content["analysis"]["overall_score"] > 0
    assert len(content["analysis"]["weak_areas"]) == 2  # Biology and Physics
    assert len(content["analysis"]["strong_areas"]) == 1  # Mathematics
    
    # Verify recommendations
    assert len(content["study_recommendations"]) == 2
    assert len(content["ar_simulations"]) >= 1  # At least one AR simulation for Science/Physics
    assert content["motivational_feedback"] != ""


def test_get_virtual_tutor_recommendations_unauthenticated(
    client: TestClient,
) -> None:
    """Test that unauthenticated requests are rejected."""
    response = client.get(
        f"{settings.API_V1_STR}/virtual-tutor/recommendations",
    )
    assert response.status_code == 401


def test_virtual_tutor_recommendations_ar_simulations(
    client: TestClient, db: Session
) -> None:
    """Test that AR simulations are suggested for science subjects."""
    user = create_random_user(db)
    
    # Add progress in science subjects
    for subject in ["Science", "Physics", "Chemistry"]:
        crud.create_student_progress(
            session=db,
            progress_in=StudentProgressCreate(
                subject=subject, topic="Basics", score=40.0, completed=False
            ),
            student_id=user.id,
        )
    
    # Get token for this user
    token = create_access_token(str(user.id))
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(
        f"{settings.API_V1_STR}/virtual-tutor/recommendations",
        headers=headers,
    )
    assert response.status_code == 200
    content = response.json()
    
    # Should have AR simulations for science subjects
    assert len(content["ar_simulations"]) >= 3
    for sim in content["ar_simulations"]:
        assert "ar_model_url" in sim
        assert sim["subject"] in ["Science", "Physics", "Chemistry"]
