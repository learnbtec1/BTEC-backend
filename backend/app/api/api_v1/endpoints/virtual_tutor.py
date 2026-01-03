"""
Virtual Tutor API Endpoints

Provides authenticated endpoints for students to get personalized
learning recommendations based on their progress.
"""

from typing import Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentUser, SessionDep
from app.virtual_tutor import get_recommendations

router = APIRouter()


@router.get("/recommendations", response_model=dict[str, Any])
def get_virtual_tutor_recommendations(
    session: SessionDep,
    current_user: CurrentUser,
) -> dict[str, Any]:
    """
    Get personalized learning recommendations for the current user.

    Analyzes student progress across all subjects and topics to provide:
    - Study recommendations for weak areas
    - AR simulation suggestions for hands-on practice
    - Motivational feedback
    - Overall performance analysis

    Requires authentication.
    """
    recommendations = get_recommendations(
        session=session,
        student_id=current_user.id,
    )
    return recommendations
