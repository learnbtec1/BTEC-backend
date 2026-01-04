import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


# Database model for user files
class UserFile(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    filename: str = Field(max_length=255)
    stored_path: str = Field(max_length=500)
    content_type: str | None = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Properties to return via API
class UserFilePublic(SQLModel):
    id: uuid.UUID
    owner_id: uuid.UUID
    filename: str
    content_type: str | None
    created_at: datetime


class UserFilesPublic(SQLModel):
    data: list[UserFilePublic]
    count: int
