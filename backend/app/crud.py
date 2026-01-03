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


def create_student_progress(
    *, session: Session, progress_in: StudentProgressCreate, student_id: uuid.UUID
) -> StudentProgress:
    db_progress = StudentProgress.model_validate(
        progress_in, update={"student_id": student_id}
    )
    session.add(db_progress)
    session.commit()
    session.refresh(db_progress)
    return db_progress


def get_student_progress(
    *, session: Session, progress_id: uuid.UUID
) -> StudentProgress | None:
    return session.get(StudentProgress, progress_id)


def update_student_progress(
    *,
    session: Session,
    db_progress: StudentProgress,
    progress_in: StudentProgressUpdate,
) -> StudentProgress:
    progress_data = progress_in.model_dump(exclude_unset=True)
    db_progress.sqlmodel_update(progress_data)
    session.add(db_progress)
    session.commit()
    session.refresh(db_progress)
    return db_progress


def list_student_progress(
    *, session: Session, student_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[StudentProgress]:
    statement = (
        select(StudentProgress)
        .where(StudentProgress.student_id == student_id)
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())
