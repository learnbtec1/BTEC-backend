from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ActivationCreate(BaseModel):
    """Schema for creating activation keys."""
    student_id: str
    student_email: str
    specialization: Optional[str] = None
    level: Optional[str] = None
    validity_days: int = 120  # default فصل دراسي تقريبي


class ActivationResponse(BaseModel):
    """Schema for activation key response."""
    token: str
    jti: str
    expires_at: datetime


class ActivateRequest(BaseModel):
    """Schema for activation request."""
    token: str
