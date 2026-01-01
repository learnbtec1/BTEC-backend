from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.btec_activation.models import ActivationKey
from app.btec_activation.services import verify_token
import jwt


def test_generate_activation_key(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Test generating an activation key."""
    data = {
        "student_id": "STU12345",
        "student_email": "student@example.com",
        "specialization": "Computer Science",
        "level": "Level 3",
        "validity_days": 120
    }
    r = client.post(
        f"{settings.API_V1_STR}/activation/admin/generate",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    response = r.json()
    assert "token" in response
    assert "jti" in response
    assert "expires_at" in response
    
    # Verify token can be decoded
    payload = verify_token(response["token"])
    assert payload["sub"] == data["student_id"]
    assert payload["email"] == data["student_email"]
    
    # Verify key is stored in database
    statement = select(ActivationKey).where(ActivationKey.jti == response["jti"])
    result = db.exec(statement)
    key = result.first()
    assert key is not None
    assert key.student_id == data["student_id"]
    assert key.student_email == data["student_email"]
    assert key.is_active is True
    assert key.is_revoked is False


def test_activate_key(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Test activating with a valid token."""
    # First generate a key
    data = {
        "student_id": "STU67890",
        "student_email": "student2@example.com",
        "specialization": "Engineering",
        "level": "Level 2",
        "validity_days": 90
    }
    r = client.post(
        f"{settings.API_V1_STR}/activation/admin/generate",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    token = r.json()["token"]
    
    # Now activate with the token
    activate_data = {"token": token}
    r = client.post(
        f"{settings.API_V1_STR}/activation/activate",
        json=activate_data,
    )
    assert r.status_code == 200
    response = r.json()
    assert response["status"] == "activated"
    assert response["student_id"] == data["student_id"]


def test_activate_invalid_token(client: TestClient) -> None:
    """Test activating with an invalid token."""
    activate_data = {"token": "invalid.token.here"}
    r = client.post(
        f"{settings.API_V1_STR}/activation/activate",
        json=activate_data,
    )
    assert r.status_code == 400
    assert "غير صالح" in r.json()["detail"]


def test_activate_expired_token(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    """Test activating with an expired token."""
    # Create a token that's already expired
    from app.btec_activation.services import SECRET_KEY, ALGORITHM
    from datetime import datetime, timedelta
    import uuid
    
    expired_payload = {
        "jti": str(uuid.uuid4()),
        "sub": "STU99999",
        "email": "expired@example.com",
        "spec": "Test",
        "level": "Level 1",
        "iat": int((datetime.utcnow() - timedelta(days=2)).timestamp()),
        "exp": int((datetime.utcnow() - timedelta(days=1)).timestamp())
    }
    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)
    
    activate_data = {"token": expired_token}
    r = client.post(
        f"{settings.API_V1_STR}/activation/activate",
        json=activate_data,
    )
    assert r.status_code == 400
    assert "غير صالح" in r.json()["detail"]


def test_activation_key_usage_tracking(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    """Test that activation key usage is tracked."""
    # Generate a key
    data = {
        "student_id": "STU11111",
        "student_email": "student3@example.com",
        "validity_days": 100
    }
    r = client.post(
        f"{settings.API_V1_STR}/activation/admin/generate",
        headers=superuser_token_headers,
        json=data,
    )
    token = r.json()["token"]
    jti = r.json()["jti"]
    
    # Get initial state
    statement = select(ActivationKey).where(ActivationKey.jti == jti)
    result = db.exec(statement)
    key = result.first()
    initial_count = key.used_count
    
    # Activate the key
    activate_data = {"token": token}
    r = client.post(
        f"{settings.API_V1_STR}/activation/activate",
        json=activate_data,
    )
    assert r.status_code == 200
    
    # Verify usage count increased
    db.expire_all()  # Refresh from database
    result = db.exec(statement)
    key = result.first()
    assert key.used_count == initial_count + 1
    assert key.last_used_at is not None
    assert key.last_used_ip is not None
