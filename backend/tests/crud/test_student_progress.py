import uuid

from sqlmodel import Session

from app import crud
from app.models import StudentProgressCreate, StudentProgressUpdate
from tests.utils.student_progress import create_random_student_progress
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def test_create_student_progress(db: Session) -> None:
    user = create_random_user(db)
    subject = "Mathematics"
    topic = "Algebra"
    score = 85.0
    completed = True
    notes = "Good progress"
    
    progress_in = StudentProgressCreate(
        subject=subject,
        topic=topic,
        score=score,
        completed=completed,
        notes=notes,
    )
    progress = crud.create_student_progress(
        session=db, progress_in=progress_in, student_id=user.id
    )
    
    assert progress.subject == subject
    assert progress.topic == topic
    assert progress.score == score
    assert progress.completed == completed
    assert progress.notes == notes
    assert progress.student_id == user.id
    assert progress.id is not None


def test_get_student_progress(db: Session) -> None:
    progress = create_random_student_progress(db)
    retrieved_progress = crud.get_student_progress(session=db, progress_id=progress.id)
    
    assert retrieved_progress is not None
    assert retrieved_progress.id == progress.id
    assert retrieved_progress.subject == progress.subject
    assert retrieved_progress.topic == progress.topic
    assert retrieved_progress.score == progress.score


def test_get_student_progress_not_found(db: Session) -> None:
    random_id = uuid.uuid4()
    progress = crud.get_student_progress(session=db, progress_id=random_id)
    assert progress is None


def test_update_student_progress(db: Session) -> None:
    progress = create_random_student_progress(db)
    new_score = 95.0
    new_completed = False
    
    progress_update = StudentProgressUpdate(
        score=new_score,
        completed=new_completed,
    )
    updated_progress = crud.update_student_progress(
        session=db, db_progress=progress, progress_in=progress_update
    )
    
    assert updated_progress.id == progress.id
    assert updated_progress.score == new_score
    assert updated_progress.completed == new_completed
    assert updated_progress.subject == progress.subject  # Unchanged


def test_list_student_progress(db: Session) -> None:
    user = create_random_user(db)
    
    # Create multiple progress entries for the user
    progress1 = crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Math", topic="Algebra", score=85.0, completed=True
        ),
        student_id=user.id,
    )
    progress2 = crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Science", topic="Physics", score=75.0, completed=False
        ),
        student_id=user.id,
    )
    
    progress_list = crud.list_student_progress(session=db, student_id=user.id)
    
    assert len(progress_list) >= 2
    progress_ids = [p.id for p in progress_list]
    assert progress1.id in progress_ids
    assert progress2.id in progress_ids


def test_list_student_progress_with_limit(db: Session) -> None:
    user = create_random_user(db)
    
    # Create multiple progress entries
    for i in range(5):
        crud.create_student_progress(
            session=db,
            progress_in=StudentProgressCreate(
                subject=f"Subject{i}",
                topic=f"Topic{i}",
                score=float(70 + i),
                completed=i % 2 == 0,
            ),
            student_id=user.id,
        )
    
    # Test with limit
    progress_list = crud.list_student_progress(
        session=db, student_id=user.id, skip=0, limit=3
    )
    assert len(progress_list) == 3
    
    # Test with skip
    progress_list_skip = crud.list_student_progress(
        session=db, student_id=user.id, skip=2, limit=3
    )
    assert len(progress_list_skip) == 3
