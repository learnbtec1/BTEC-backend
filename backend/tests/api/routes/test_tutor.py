"""Integration tests for virtual tutor API endpoint."""

from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.models import StudentProgressCreate
from tests.utils.user import create_random_user


def test_get_tutor_recommendations_authenticated(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Test getting recommendations requires authentication."""
    # Authenticated request should work
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200


def test_get_tutor_recommendations_unauthenticated(client: TestClient) -> None:
    """Test that unauthenticated requests are rejected."""
    response = client.get(f"{settings.API_V1_STR}/tutor/recommendations")
    assert response.status_code == 401


def test_get_tutor_recommendations_no_progress(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test recommendations when user has no progress data."""
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data
    assert isinstance(data["data"], list)
    assert data["count"] == len(data["data"])


def test_get_tutor_recommendations_with_struggling_modules(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Test recommendations when user has struggling modules."""
    # Get the current user from the token
    from tests.utils.user import authentication_token_from_email
    from app.core.config import settings as app_settings
    
    # Get user associated with the token
    user = crud.get_user_by_email(session=db, email=app_settings.EMAIL_TEST_USER)
    assert user is not None
    
    # Create some struggling progress for the user
    struggling_module = StudentProgressCreate(
        module_name="difficult_topic",
        progress=35,
        struggling=True,
        last_score=30.0,
        attempts=4,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=struggling_module
    )
    
    low_progress_module = StudentProgressCreate(
        module_name="challenging_subject",
        progress=50,
        struggling=False,
        last_score=48.0,
        attempts=2,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=low_progress_module
    )
    
    # Get recommendations
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    data = response.json()
    
    assert data["count"] >= 2
    assert len(data["data"]) >= 2
    
    # Verify structure of recommendations
    for rec in data["data"]:
        assert "module_name" in rec
        assert "current_progress" in rec
        assert "last_score" in rec
        assert "attempts" in rec
        assert "struggling" in rec
        assert "recommended_action" in rec
        assert "resources" in rec
        assert isinstance(rec["resources"], list)


def test_get_tutor_recommendations_custom_threshold(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Test recommendations with custom threshold parameter."""
    # Get user
    from app.core.config import settings as app_settings
    user = crud.get_user_by_email(session=db, email=app_settings.EMAIL_TEST_USER)
    assert user is not None
    
    # Create module with 70% progress
    progress_in = StudentProgressCreate(
        module_name="module_at_70",
        progress=70,
        struggling=False,
        last_score=72.0,
        attempts=1,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    # With default threshold 60, should not appear
    response_60 = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=60",
        headers=normal_user_token_headers,
    )
    assert response_60.status_code == 200
    data_60 = response_60.json()
    module_names_60 = {r["module_name"] for r in data_60["data"]}
    assert "module_at_70" not in module_names_60
    
    # With threshold 80, should appear
    response_80 = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=80",
        headers=normal_user_token_headers,
    )
    assert response_80.status_code == 200
    data_80 = response_80.json()
    module_names_80 = {r["module_name"] for r in data_80["data"]}
    assert "module_at_70" in module_names_80


def test_get_tutor_recommendations_invalid_threshold(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    """Test that invalid threshold values are rejected."""
    # Threshold too low
    response_low = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=-1",
        headers=normal_user_token_headers,
    )
    assert response_low.status_code == 400
    
    # Threshold too high
    response_high = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations?threshold=101",
        headers=normal_user_token_headers,
    )
    assert response_high.status_code == 400


def test_get_tutor_recommendations_user_isolation(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    superuser_token_headers: dict[str, str],
    db: Session,
) -> None:
    """Test that users only see their own recommendations."""
    from app.core.config import settings as app_settings
    
    # Get normal user
    normal_user = crud.get_user_by_email(session=db, email=app_settings.EMAIL_TEST_USER)
    assert normal_user is not None
    
    # Get superuser
    superuser = crud.get_user_by_email(session=db, email=app_settings.FIRST_SUPERUSER)
    assert superuser is not None
    
    # Create progress for normal user
    normal_progress = StudentProgressCreate(
        module_name="normal_user_module",
        progress=40,
        struggling=True,
        attempts=2,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=normal_user.id, progress_in=normal_progress
    )
    
    # Create progress for superuser
    super_progress = StudentProgressCreate(
        module_name="superuser_module",
        progress=45,
        struggling=True,
        attempts=1,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=superuser.id, progress_in=super_progress
    )
    
    # Normal user should only see their own module
    normal_response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations",
        headers=normal_user_token_headers,
    )
    assert normal_response.status_code == 200
    normal_data = normal_response.json()
    normal_modules = {r["module_name"] for r in normal_data["data"]}
    assert "normal_user_module" in normal_modules
    assert "superuser_module" not in normal_modules
    
    # Superuser should only see their own module
    super_response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations",
        headers=superuser_token_headers,
    )
    assert super_response.status_code == 200
    super_data = super_response.json()
    super_modules = {r["module_name"] for r in super_data["data"]}
    assert "superuser_module" in super_modules
    assert "normal_user_module" not in super_modules


def test_get_tutor_recommendations_response_structure(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    """Test the structure of the recommendations response."""
    from app.core.config import settings as app_settings
    
    user = crud.get_user_by_email(session=db, email=app_settings.EMAIL_TEST_USER)
    assert user is not None
    
    # Create a struggling module
    progress_in = StudentProgressCreate(
        module_name="test_module",
        progress=45,
        struggling=True,
        last_score=42.5,
        attempts=3,
    )
    crud.create_or_update_student_progress(
        session=db, user_id=user.id, progress_in=progress_in
    )
    
    response = client.get(
        f"{settings.API_V1_STR}/tutor/recommendations",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    data = response.json()
    
    # Check top-level structure
    assert "data" in data
    assert "count" in data
    assert isinstance(data["data"], list)
    assert isinstance(data["count"], int)
    assert data["count"] > 0
    
    # Check individual recommendation structure
    rec = data["data"][0]
    assert isinstance(rec["module_name"], str)
    assert isinstance(rec["current_progress"], int)
    assert rec["last_score"] is None or isinstance(rec["last_score"], (int, float))
    assert isinstance(rec["attempts"], int)
    assert isinstance(rec["struggling"], bool)
    assert isinstance(rec["recommended_action"], str)
    assert isinstance(rec["resources"], list)
    assert len(rec["resources"]) > 0
    assert all(isinstance(r, str) for r in rec["resources"])
