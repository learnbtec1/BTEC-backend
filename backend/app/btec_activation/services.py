import os
from datetime import datetime, timedelta

import jwt
from sqlmodel import Session, select

from app.btec_activation.models import ActivationKey

SECRET_KEY = os.getenv("ACTIVATION_SECRET", "change-me-in-prod")
ALGORITHM = "HS256"


def generate_token_payload(
    jti: str,
    student_id: str,
    email: str,
    specialization: str,
    level: str,
    validity_days: int
) -> dict:
    """Generate JWT payload for activation token."""
    iat = datetime.utcnow()
    exp = iat + timedelta(days=validity_days)
    return {
        "jti": jti,
        "sub": student_id,
        "email": email,
        "spec": specialization,
        "level": level,
        "iat": int(iat.timestamp()),
        "exp": int(exp.timestamp())
    }


def create_activation_token(
    jti: str,
    student_id: str,
    email: str,
    specialization: str,
    level: str,
    validity_days: int
) -> tuple[str, datetime]:
    """Create a JWT activation token."""
    payload = generate_token_payload(
        jti, student_id, email, specialization, level, validity_days
    )
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    expires_at = datetime.utcfromtimestamp(payload["exp"])
    return token, expires_at


async def store_activation_key(
    session: Session,
    jti: str,
    student_id: str,
    email: str,
    specialization: str,
    level: str,
    expires_at: datetime,
    metadata: dict | None = None
) -> ActivationKey:
    """Store activation key in database."""
    key = ActivationKey(
        jti=jti,
        student_id=student_id,
        student_email=email,
        specialization=specialization,
        level=level,
        expires_at=expires_at,
        metadata=metadata or {}
    )
    session.add(key)
    session.commit()
    session.refresh(key)
    return key


def verify_token(token: str) -> dict:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise


async def consume_activation_token(
    session: Session,
    jti: str,
    used_ip: str | None = None
) -> ActivationKey | None:
    """Consume activation token and update usage stats."""
    q = select(ActivationKey).where(ActivationKey.jti == jti)
    res = session.exec(q)
    key = res.first()
    if not key:
        return None
    if key.is_revoked or not key.is_active:
        return key
    key.used_count += 1
    key.last_used_at = datetime.utcnow()
    key.last_used_ip = used_ip
    session.commit()
    session.refresh(key)
    return key
