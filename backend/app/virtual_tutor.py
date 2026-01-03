"""Virtual Tutor module for providing personalized remediation recommendations."""

from sqlmodel import Session

from app.crud import get_struggling_modules_for_user
from app.models import User


def recommend_remediation(
    session: Session, user: User, threshold: int = 60
) -> list[dict]:
    """
    Recommend remediation resources based on student progress.

    Args:
        session: Database session
        user: The user/student to get recommendations for
        threshold: Progress percentage threshold below which to recommend help (default: 60)

    Returns:
        List of recommendation dictionaries with module info and suggested actions
    """
    # Get modules where student is struggling
    struggling_modules = get_struggling_modules_for_user(
        session=session, user_id=user.id, progress_threshold=threshold
    )

    recommendations = []
    for progress in struggling_modules:
        recommendation = {
            "module_name": progress.module_name,
            "current_progress": progress.progress_percentage,
            "struggling": progress.struggling,
            "recommendations": _generate_module_recommendations(progress),
        }
        recommendations.append(recommendation)

    return recommendations


def _generate_module_recommendations(progress) -> list[str]:
    """
    Generate specific recommendations based on progress metrics.

    Args:
        progress: StudentProgress object

    Returns:
        List of actionable recommendation strings
    """
    recommendations = []
    progress_pct = progress.progress_percentage

    # Base recommendations based on progress level
    if progress_pct < 30:
        recommendations.extend(
            [
                f"Review fundamental concepts for {progress.module_name}",
                "Schedule a 1-on-1 tutoring session",
                "Complete introductory exercises and quizzes",
            ]
        )
    elif progress_pct < 60:
        recommendations.extend(
            [
                f"Practice intermediate exercises for {progress.module_name}",
                "Review video tutorials for challenging topics",
                "Join a study group for peer learning",
            ]
        )
    else:
        # Progress >= 60 but marked as struggling
        recommendations.extend(
            [
                f"Focus on advanced topics in {progress.module_name}",
                "Complete practice problems to reinforce understanding",
                "Review recent errors and misconceptions",
            ]
        )

    # Add AR-specific recommendations
    recommendations.append(
        f"Explore AR simulations and 3D models for {progress.module_name}"
    )

    return recommendations
