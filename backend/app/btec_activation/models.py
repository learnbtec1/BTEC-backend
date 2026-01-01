import uuid
from datetime import UTC, datetime

from sqlmodel import JSON, Column, Field, SQLModel, String


class ActivationKey(SQLModel, table=True):
    """Model for storing activation keys."""
    id: int | None = Field(default=None, primary_key=True)
    jti: str = Field(
        sa_column=Column(String, unique=True, index=True),
        default_factory=lambda: str(uuid.uuid4())
    )
    student_id: str | None = Field(index=True, default=None)
    student_email: str | None = Field(index=True, default=None)
    specialization: str | None = None
    level: str | None = None
    issued_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    expires_at: datetime
    is_active: bool = Field(default=True)
    is_revoked: bool = Field(default=False)
    used_count: int = Field(default=0)
    last_used_at: datetime | None = None
    last_used_ip: str | None = None
    metadata: dict | None = Field(default=None, sa_column=Column(JSON))
