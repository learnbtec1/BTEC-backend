from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, String, DateTime, Boolean, JSON
import uuid


class ActivationKey(SQLModel, table=True):
    """Model for storing activation keys."""
    id: Optional[int] = Field(default=None, primary_key=True)
    jti: str = Field(
        sa_column=Column(String, unique=True, index=True),
        default_factory=lambda: str(uuid.uuid4())
    )
    student_id: Optional[str] = Field(index=True, default=None)
    student_email: Optional[str] = Field(index=True, default=None)
    specialization: Optional[str] = None
    level: Optional[str] = None
    issued_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    is_active: bool = Field(default=True)
    is_revoked: bool = Field(default=False)
    used_count: int = Field(default=0)
    last_used_at: Optional[datetime] = None
    last_used_ip: Optional[str] = None
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))
