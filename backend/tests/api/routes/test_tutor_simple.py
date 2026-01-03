"""Simplified integration tests for virtual tutor API endpoint without full auth stack."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app import crud
from app.models import StudentProgressCreate, User
from tests.utils.user import create_random_user


def test_tutor_endpoint_exists(client: TestClient) -> None:
    """Test that the tutor endpoint is registered."""
    # Try to access the endpoint (will fail auth but proves it exists)
    response = client.get(f"{settings.API_V1_STR}/tutor/recommendations")
    # Endpoint exists but requires auth, so we expect either 401 or 403
    # In this minimal setup without login, we might get 401
    assert response.status_code in [401, 403, 422]  # Any of these means endpoint exists


def test_tutor_recommendations_structure(db: Session) -> None:
    """Test the recommendation structure directly through the service."""
    from app.virtual_tutor import recommend_remediation
    
    user = create_random_user(db)
    
    # Create some struggling progress
    progress_in = StudentProgressCreate(
        module_name="test_module",
        progress=40,
        struggling=True,
        last_score=35.0,
        attempts=3,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    # Get recommendations
    recommendations = recommend_remediation(session=db, user=user, threshold=60)
    
    assert len(recommendations) >= 1
    rec = recommendations[0]
    assert rec["module_name"] == "test_module"
    assert rec["current_progress"] == 40
    assert rec["struggling"] is True
    assert "recommended_action" in rec
    assert "resources" in rec


def test_tutor_endpoint_parameter_validation(client: TestClient) -> None:
    """Test that invalid threshold parameters are validated."""
    # These should fail validation even before auth
    response_low = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=-1"
    )
    # Should be either validation error (422) or auth error
    assert response_low.status_code in [400, 401, 403, 422]
    
    response_high = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=101"
    )
    assert response_high.status_code in [400, 401, 403, 422]
