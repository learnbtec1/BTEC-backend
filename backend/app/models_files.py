import uuid
from datetime import datetime, timezone

from sqlmodel import Field, Relationship, SQLModel


# Database model for file uploads
class UserFile(SQLModel, table=True):
    """Model for storing user uploaded files metadata."""
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    original_filename: str = Field(max_length=255)
    stored_path: str = Field(max_length=512)
    content_type: str = Field(max_length=128)
    size: int  # Size in bytes
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    # Relationship
    owner: "User | None" = Relationship(back_populates="files")  # type: ignore


# Properties to return via API
class UserFilePublic(SQLModel):
    """Public response model for file metadata."""
    
    id: uuid.UUID
    owner_id: uuid.UUID
    original_filename: str
    stored_path: str
    content_type: str
    size: int
    created_at: datetime


class UserFilesPublic(SQLModel):
    """Response model for list of files."""
    
    data: list[UserFilePublic]
    count: int
