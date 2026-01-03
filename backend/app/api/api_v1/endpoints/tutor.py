"""Virtual Tutor API endpoints."""

from typing import Any

from fastapi import APIRouter, Query

from app.api.deps import CurrentUser, SessionDep
from app.virtual_tutor import recommend_remediation

router = APIRouter()


@router.get("/recommendations")
def get_tutor_recommendations(
    session: SessionDep,
    current_user: CurrentUser,
    threshold: int = Query(default=60, ge=0, le=100),
) -> Any:
    """
    Get personalized remediation recommendations for the current user.

    Args:
        session: Database session (injected)
        current_user: Currently authenticated user (injected)
        threshold: Progress percentage threshold for struggling modules (default: 60)

    Returns:
        Dictionary with recommendations list
    """
    recommendations = recommend_remediation(
        session=session, user=current_user, threshold=threshold
    )
    return {
        "user_id": str(current_user.id),
        "user_email": current_user.email,
        "threshold": threshold,
        "recommendations": recommendations,
    }
