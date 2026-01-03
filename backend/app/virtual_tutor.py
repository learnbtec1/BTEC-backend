"""Virtual tutor logic for recommending remediation based on student progress."""

from sqlmodel import Session

from app import crud
from app.models import User


def recommend_remediation(
    *, session: Session, user: User, threshold: int = 60
) -> list[dict]:
    """
    Recommend remediation for struggling modules.

    Args:
        session: Database session
        user: The user to get recommendations for
        threshold: Progress threshold below which a module is considered struggling (default: 60)

    Returns:
        List of dictionaries containing module info and recommended actions
    """
    struggling_modules = crud.get_struggling_modules_for_user(
        session=session, user_id=user.id, progress_threshold=threshold
    )

    recommendations = []
    for module_progress in struggling_modules:
        recommendation = {
            "module_name": module_progress.module_name,
            "current_progress": module_progress.progress,
            "last_score": module_progress.last_score,
            "attempts": module_progress.attempts,
            "struggling": module_progress.struggling,
            "recommended_action": _get_recommended_action(module_progress),
            "resources": _get_recommended_resources(module_progress),
        }
        recommendations.append(recommendation)

    return recommendations


def _get_recommended_action(module_progress) -> str:
    """Generate a recommended action based on student progress."""
    if module_progress.progress < 30:
        return "Review fundamentals and practice basic concepts"
    elif module_progress.progress < 50:
        return "Focus on core topics and complete practice exercises"
    elif module_progress.progress < 70:
        return "Work on intermediate concepts and review missed topics"
    else:
        return "Fine-tune understanding with targeted practice"


def _get_recommended_resources(module_progress) -> list[str]:
    """Generate a list of recommended resources based on progress."""
    resources = []

    if module_progress.attempts > 3:
        resources.append("Schedule a tutoring session for personalized help")

    if module_progress.last_score and module_progress.last_score < 50:
        resources.append("Review video tutorials for this module")
        resources.append("Complete interactive practice problems")

    if module_progress.progress < 40:
        resources.append("Start with beginner-level materials")
        resources.append("Join study group for peer support")
    elif module_progress.progress < 70:
        resources.append("Access supplementary reading materials")
        resources.append("Practice with real-world examples")

    # Default resource
    if not resources:
        resources.append("Continue regular practice and review")

    return resources
