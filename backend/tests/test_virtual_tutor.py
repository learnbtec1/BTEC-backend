from sqlmodel import Session

from app import crud, virtual_tutor
from app.models import StudentProgressCreate
from tests.utils.user import create_random_user


def test_analyze_student_progress_no_data(db: Session) -> None:
    """Test analysis with no progress data."""
    user = create_random_user(db)
    
    analysis = virtual_tutor.analyze_student_progress(
        session=db, student_id=user.id
    )
    
    assert analysis["total_topics"] == 0
    assert analysis["overall_score"] == 0.0
    assert analysis["completion_rate"] == 0.0
    assert len(analysis["weak_areas"]) == 0
    assert len(analysis["strong_areas"]) == 0


def test_analyze_student_progress_with_data(db: Session) -> None:
    """Test analysis with various progress data."""
    user = create_random_user(db)
    
    # Add varied progress entries
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Math", topic="Algebra", score=45.0, completed=True
        ),
        student_id=user.id,
    )
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Science", topic="Biology", score=85.0, completed=True
        ),
        student_id=user.id,
    )
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="English", topic="Literature", score=70.0, completed=False
        ),
        student_id=user.id,
    )
    
    analysis = virtual_tutor.analyze_student_progress(
        session=db, student_id=user.id
    )
    
    assert analysis["total_topics"] == 3
    assert analysis["overall_score"] == 66.67  # (45 + 85 + 70) / 3
    assert analysis["completion_rate"] == 66.67  # 2 out of 3 completed
    assert len(analysis["weak_areas"]) == 1  # Math with 45
    assert len(analysis["strong_areas"]) == 1  # Science with 85


def test_get_recommendations_weak_areas(db: Session) -> None:
    """Test recommendations generation for weak areas."""
    user = create_random_user(db)
    
    # Add progress with weak score
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Physics", topic="Mechanics", score=35.0, completed=False
        ),
        student_id=user.id,
    )
    
    recommendations = virtual_tutor.get_recommendations(
        session=db, student_id=user.id
    )
    
    assert len(recommendations["study_recommendations"]) == 1
    study_rec = recommendations["study_recommendations"][0]
    assert study_rec["subject"] == "Physics"
    assert study_rec["topic"] == "Mechanics"
    assert study_rec["priority"] == "high"  # Score < 40


def test_get_recommendations_ar_simulations(db: Session) -> None:
    """Test AR simulation recommendations for science subjects."""
    user = create_random_user(db)
    
    # Add progress in science subject with weak score
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Chemistry", topic="Organic Chemistry", score=50.0, completed=False
        ),
        student_id=user.id,
    )
    
    recommendations = virtual_tutor.get_recommendations(
        session=db, student_id=user.id
    )
    
    # Should suggest AR simulation for Chemistry
    assert len(recommendations["ar_simulations"]) == 1
    ar_sim = recommendations["ar_simulations"][0]
    assert ar_sim["subject"] == "Chemistry"
    assert ar_sim["topic"] == "Organic Chemistry"
    assert "ar_model_url" in ar_sim
    assert ar_sim["difficulty"] == "intermediate"  # Score is 50


def test_get_recommendations_motivational_feedback(db: Session) -> None:
    """Test motivational feedback generation."""
    user = create_random_user(db)
    
    # Test excellent performance (>= 80)
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Math", topic="Algebra", score=90.0, completed=True
        ),
        student_id=user.id,
    )
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Science", topic="Biology", score=85.0, completed=True
        ),
        student_id=user.id,
    )
    
    recommendations = virtual_tutor.get_recommendations(
        session=db, student_id=user.id
    )
    
    assert "Excellent work" in recommendations["motivational_feedback"]


def test_get_recommendations_low_completion_rate(db: Session) -> None:
    """Test feedback for low completion rate."""
    user = create_random_user(db)
    
    # Add many incomplete topics
    for i in range(10):
        crud.create_student_progress(
            session=db,
            progress_in=StudentProgressCreate(
                subject=f"Subject{i}",
                topic=f"Topic{i}",
                score=70.0,
                completed=i < 3,  # Only 3 out of 10 completed (30%)
            ),
            student_id=user.id,
        )
    
    recommendations = virtual_tutor.get_recommendations(
        session=db, student_id=user.id
    )
    
    # Should mention completion rate in feedback
    assert "completion" in recommendations["motivational_feedback"].lower()
    assert recommendations["analysis"]["completion_rate"] == 30.0


def test_ar_simulation_url_format(db: Session) -> None:
    """Test that AR simulation URLs are properly formatted."""
    user = create_random_user(db)
    
    crud.create_student_progress(
        session=db,
        progress_in=StudentProgressCreate(
            subject="Biology", topic="Cell Structure", score=40.0, completed=False
        ),
        student_id=user.id,
    )
    
    recommendations = virtual_tutor.get_recommendations(
        session=db, student_id=user.id
    )
    
    assert len(recommendations["ar_simulations"]) == 1
    ar_sim = recommendations["ar_simulations"][0]
    # Check URL is properly formatted with lowercase and hyphens
    assert ar_sim["ar_model_url"] == "/ar/simulations/biology/cell-structure"
