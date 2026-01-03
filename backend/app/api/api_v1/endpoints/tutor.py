"""Virtual tutor API endpoints."""

from fastapi import APIRouter, HTTPException
from sqlmodel import Session

from app.api.deps import CurrentUser, SessionDep
from app.virtual_tutor import recommend_remediation

router = APIRouter()


@router.get("/recommendations")
def get_tutor_recommendations(
    session: SessionDep,
    current_user: CurrentUser,
    threshold: int = 60,
) -> dict:
    """
    Get personalized learning recommendations based on student progress.

    Args:
        session: Database session dependency
        current_user: Currently authenticated user
        threshold: Progress threshold (0-100) below which modules are considered struggling

    Returns:
        Dictionary containing recommendations list and count
    """
    if threshold < 0 or threshold > 100:
        raise HTTPException(
            status_code=400, detail="Threshold must be between 0 and 100"
        )

    recommendations = recommend_remediation(
        session=session, user=current_user, threshold=threshold
    )

    return {"data": recommendations, "count": len(recommendations)}
