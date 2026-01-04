import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


# Database model for student progress tracking
class StudentProgress(SQLModel, table=True):
    """Model for tracking student progress through lessons."""
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    lesson_id: uuid.UUID | None = Field(default=None)
    progress_percentage: int = Field(default=0)
    last_score: float | None = Field(default=None)
    attempts: int = Field(default=0)
    struggling: bool = Field(default=False)
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# Create model for API
class StudentProgressCreate(SQLModel):
    """Model for creating student progress."""
    
    user_id: uuid.UUID
    lesson_id: uuid.UUID | None = None
    progress_percentage: int = 0
    last_score: float | None = None
    attempts: int = 0
    struggling: bool = False


# Update model for API
class StudentProgressUpdate(SQLModel):
    """Model for updating student progress."""
    
    lesson_id: uuid.UUID | None = None
    progress_percentage: int | None = None
    last_score: float | None = None
    attempts: int | None = None
    struggling: bool | None = None


# Response model for API
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
