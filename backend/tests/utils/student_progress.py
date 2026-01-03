from sqlmodel import Session

from app import crud
from app.models import StudentProgress, StudentProgressCreate
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def create_random_student_progress(db: Session) -> StudentProgress:
    """Create a random student progress entry for testing."""
    user = create_random_user(db)
    student_id = user.id
    assert student_id is not None
    
    subject = random_lower_string()
    topic = random_lower_string()
    score = 75.5
    completed = True
    notes = random_lower_string()
    
    progress_in = StudentProgressCreate(
        subject=subject,
        topic=topic,
        score=score,
        completed=completed,
        notes=notes,
    )
    return crud.create_student_progress(
        session=db, progress_in=progress_in, student_id=student_id
    )
