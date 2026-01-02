import uuid
from datetime import datetime

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    username: str = Field(unique=True, index=True, max_length=50)
    role: str = Field(default="student", max_length=20)  # "student" or "teacher"


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=4, max_length=128)  # Allow shorter passwords for testing


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=4, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)
    username: str = Field(max_length=50)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=4, max_length=128)
    username: str | None = Field(default=None, max_length=50)  # type: ignore
    role: str | None = Field(default=None, max_length=20)  # type: ignore


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    assignments: list["Assignment"] = Relationship(back_populates="student", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=4, max_length=128)


# Assignment models
class AssignmentBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    grade: float | None = None
    comments: str | None = Field(default=None, max_length=1000)
    status: str | None = Field(default=None, max_length=20)


class Assignment(AssignmentBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    student_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    teacher_id: uuid.UUID | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")
    file_path: str = Field(max_length=500)
    file_name: str = Field(max_length=255)
    file_size: int  # Size in bytes
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    graded_at: datetime | None = None
    grade: float | None = None
    status: str = Field(default="pending", max_length=20)  # "pending" or "graded"
    comments: str | None = Field(default=None, max_length=1000)
    
    student: User | None = Relationship(
        back_populates="assignments",
        sa_relationship_kwargs={"foreign_keys": "[Assignment.student_id]"}
    )


class AssignmentPublic(AssignmentBase):
    id: uuid.UUID
    student_id: uuid.UUID
    teacher_id: uuid.UUID | None
    file_name: str
    file_size: int
    uploaded_at: datetime
    graded_at: datetime | None
    grade: float | None
    status: str
    comments: str | None


class AssignmentsPublic(SQLModel):
    data: list[AssignmentPublic]
    count: int


class AssignmentStats(SQLModel):
    total_assignments: int
    pending_assignments: int
    graded_assignments: int
    average_grade: float | None
