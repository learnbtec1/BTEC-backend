import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


# Database model for student progress tracking
class StudentProgress(SQLModel, table=True):
    """Model for tracking student learning progress."""
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    lesson_id: uuid.UUID | None = Field(default=None, nullable=True)
    progress_percentage: int = Field(default=0, ge=0, le=100)
    last_score: float | None = Field(default=None, nullable=True)
    attempts: int = Field(default=0, ge=0)
    struggling: bool = Field(default=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# Properties to receive on creation
class StudentProgressCreate(SQLModel):
    """Schema for creating student progress."""
    
    user_id: uuid.UUID
    lesson_id: uuid.UUID | None = None
    progress_percentage: int = Field(default=0, ge=0, le=100)
    last_score: float | None = None
    attempts: int = Field(default=0, ge=0)
    struggling: bool = False


# Properties to receive on update
class StudentProgressUpdate(SQLModel):
    """Schema for updating student progress."""
    
    lesson_id: uuid.UUID | None = None
    progress_percentage: int | None = Field(default=None, ge=0, le=100)
    last_score: float | None = None
    attempts: int | None = Field(default=None, ge=0)
    struggling: bool | None = None


# Properties to return via API
class StudentProgressPublic(SQLModel):
    """Public response model for student progress."""
    
    id: uuid.UUID
    user_id: uuid.UUID
    lesson_id: uuid.UUID | None
    progress_percentage: int
    last_score: float | None
    attempts: int
    struggling: bool
    updated_at: datetime


class StudentProgressList(SQLModel):
    """Response model for list of progress records."""
    
    data: list[StudentProgressPublic]
    count: int
