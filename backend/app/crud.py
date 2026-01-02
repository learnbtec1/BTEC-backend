import uuid
from typing import Any
from datetime import datetime

from sqlmodel import Session, select, func

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate, Assignment, AssignmentCreate, AssignmentUpdate


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


def get_user_by_username(*, session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
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


# Assignment CRUD operations
def create_assignment(
    *,
    session: Session,
    assignment_in: AssignmentCreate,
    student_id: uuid.UUID,
    file_path: str,
    file_name: str,
    file_size: int,
) -> Assignment:
    db_assignment = Assignment.model_validate(
        assignment_in,
        update={
            "student_id": student_id,
            "file_path": file_path,
            "file_name": file_name,
            "file_size": file_size,
        },
    )
    session.add(db_assignment)
    session.commit()
    session.refresh(db_assignment)
    return db_assignment


def get_assignment(*, session: Session, assignment_id: uuid.UUID) -> Assignment | None:
    return session.get(Assignment, assignment_id)


def get_student_assignments(
    *, session: Session, student_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[Assignment]:
    statement = (
        select(Assignment)
        .where(Assignment.student_id == student_id)
        .order_by(Assignment.uploaded_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def get_all_assignments(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[Assignment]:
    statement = (
        select(Assignment)
        .order_by(Assignment.uploaded_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def update_assignment(
    *, session: Session, db_assignment: Assignment, assignment_in: AssignmentUpdate
) -> Assignment:
    assignment_data = assignment_in.model_dump(exclude_unset=True)
    
    # If grading, set graded_at timestamp and status
    if "grade" in assignment_data and assignment_data["grade"] is not None:
        assignment_data["graded_at"] = datetime.utcnow()
        assignment_data["status"] = "graded"
    
    db_assignment.sqlmodel_update(assignment_data)
    session.add(db_assignment)
    session.commit()
    session.refresh(db_assignment)
    return db_assignment


def get_assignment_stats(*, session: Session, student_id: uuid.UUID | None = None) -> dict:
    """Get assignment statistics for a student or all students"""
    base_query = select(Assignment)
    
    if student_id:
        base_query = base_query.where(Assignment.student_id == student_id)
    
    # Total assignments
    total = session.exec(
        select(func.count()).select_from(Assignment).where(
            Assignment.student_id == student_id if student_id else True
        )
    ).one()
    
    # Pending assignments
    pending = session.exec(
        select(func.count()).select_from(Assignment).where(
            Assignment.status == "pending",
            Assignment.student_id == student_id if student_id else True,
        )
    ).one()
    
    # Graded assignments
    graded = session.exec(
        select(func.count()).select_from(Assignment).where(
            Assignment.status == "graded",
            Assignment.student_id == student_id if student_id else True,
        )
    ).one()
    
    # Average grade
    avg_grade = session.exec(
        select(func.avg(Assignment.grade)).where(
            Assignment.grade.isnot(None),
            Assignment.student_id == student_id if student_id else True,
        )
    ).one()
    
    return {
        "total_assignments": total,
        "pending_assignments": pending,
        "graded_assignments": graded,
        "average_grade": float(avg_grade) if avg_grade else None,
    }
