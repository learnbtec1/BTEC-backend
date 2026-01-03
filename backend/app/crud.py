import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Item,
    ItemCreate,
    StudentProgress,
    StudentProgressCreate,
    StudentProgressUpdate,
    User,
    UserCreate,
    UserUpdate,
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# StudentProgress CRUD functions
def get_student_progress_for_user(
    *, session: Session, user_id: uuid.UUID
) -> list[StudentProgress]:
    """Get all student progress records for a user."""
    statement = select(StudentProgress).where(StudentProgress.user_id == user_id)
    return list(session.exec(statement).all())


def get_student_progress_by_module(
    *, session: Session, user_id: uuid.UUID, module_name: str
) -> StudentProgress | None:
    """Get student progress for a specific module."""
    statement = select(StudentProgress).where(
        StudentProgress.user_id == user_id, StudentProgress.module_name == module_name
    )
    return session.exec(statement).first()


def create_or_update_student_progress(
    *, session: Session, user_id: uuid.UUID, progress_in: StudentProgressCreate
) -> StudentProgress:
    """Create or update student progress for a module."""
    # Check if progress already exists for this user and module
    existing = get_student_progress_by_module(
        session=session, user_id=user_id, module_name=progress_in.module_name
    )

    if existing:
        # Update existing progress
        progress_data = progress_in.model_dump(exclude_unset=True)
        existing.sqlmodel_update(progress_data)
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    else:
        # Create new progress record
        db_progress = StudentProgress.model_validate(
            progress_in, update={"user_id": user_id}
        )
        session.add(db_progress)
        session.commit()
        session.refresh(db_progress)
        return db_progress


def set_student_progress_fields(
    *,
    session: Session,
    progress_obj: StudentProgress,
    progress_update: StudentProgressUpdate,
) -> StudentProgress:
    """Update specific fields of a student progress record."""
    progress_data = progress_update.model_dump(exclude_unset=True)
    progress_obj.sqlmodel_update(progress_data)
    session.add(progress_obj)
    session.commit()
    session.refresh(progress_obj)
    return progress_obj


def get_struggling_modules_for_user(
    *, session: Session, user_id: uuid.UUID, progress_threshold: int = 60
) -> list[StudentProgress]:
    """Get modules where student is struggling (progress < threshold or struggling flag set)."""
    statement = select(StudentProgress).where(
        StudentProgress.user_id == user_id,
        StudentProgress.struggling
        | (StudentProgress.progress_percentage < progress_threshold),
    )
    return list(session.exec(statement).all())
