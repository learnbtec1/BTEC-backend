from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models_progress import StudentProgress

router = APIRouter()


# Request/Response models
class AssistantQueryRequest(BaseModel):
    """Request model for assistant queries."""
    prompt: str
    context: str | None = None


class AssistantQueryResponse(BaseModel):
    """Response model for assistant queries."""
    answer: str
    recommendations: list[str]
    actions: list[str]


@router.post("/query", response_model=AssistantQueryResponse)
def query_assistant(
    session: SessionDep,
    current_user: CurrentUser,
    request: AssistantQueryRequest,
) -> AssistantQueryResponse:
    """
    Query the Keitagorus AI assistant.
    
    This is a mock implementation that returns deterministic recommendations
    based on keywords and student progress. In production, this would integrate
    with actual AI models and more sophisticated logic.
    
    WebSocket streaming endpoint path: /api/v1/assistant/stream (to be implemented)
    """
    prompt_lower = request.prompt.lower()
    
    # Get student progress for contextual recommendations
    statement = select(StudentProgress).where(StudentProgress.user_id == current_user.id)
    progress_records = session.exec(statement).all()
    
    # Analyze student progress
    struggling_lessons = [p for p in progress_records if p.struggling]
    low_score_lessons = [p for p in progress_records if p.last_score and p.last_score < 60]
    
    # Generate mock response based on keywords
    answer = ""
    recommendations = []
    actions = []
    
    # Keyword-based responses
    if "help" in prompt_lower or "stuck" in prompt_lower:
        answer = "I'm here to help! I can assist you with understanding concepts, reviewing materials, and practicing problems."
        recommendations.extend([
            "Review the lesson materials for better understanding",
            "Try the practice exercises to reinforce your knowledge",
            "Consider watching the supplementary video tutorial",
        ])
        actions.extend([
            "open_lesson_materials",
            "start_practice_quiz",
        ])
    
    elif "practice" in prompt_lower or "quiz" in prompt_lower:
        answer = "Practice is key to mastering the material! I can help you find relevant practice exercises."
        recommendations.extend([
            "Start with easier problems to build confidence",
            "Focus on areas where you struggled previously",
            "Take regular breaks to maintain focus",
        ])
        actions.extend([
            "start_practice_quiz",
            "view_past_attempts",
        ])
    
    elif "progress" in prompt_lower or "score" in prompt_lower:
        if progress_records:
            avg_score = sum(p.last_score or 0 for p in progress_records) / len(progress_records)
            answer = f"You've completed {len(progress_records)} lessons with an average score of {avg_score:.1f}%."
            
            if struggling_lessons:
                answer += f" I notice you're struggling with {len(struggling_lessons)} lesson(s)."
                recommendations.append("Consider reviewing the lessons where you're struggling")
            
            if low_score_lessons:
                recommendations.append("Focus on improving scores in lessons where you scored below 60%")
        else:
            answer = "You haven't started any lessons yet. Let's get started!"
            recommendations.append("Begin with the introductory lesson")
        
        actions.extend([
            "view_progress_dashboard",
            "view_detailed_analytics",
        ])
    
    else:
        # Default response
        answer = "I'm Keitagorus (قيتاغورس), your AI learning assistant. I can help you with lessons, practice, and tracking your progress."
        recommendations.extend([
            "Ask me about your progress",
            "Request practice exercises",
            "Get help with difficult concepts",
        ])
        actions.extend([
            "view_available_lessons",
            "start_new_lesson",
        ])
    
    # Add context-aware recommendations if struggling
    if struggling_lessons and "help" not in prompt_lower:
        recommendations.append(f"You have {len(struggling_lessons)} lesson(s) that need attention")
    
    return AssistantQueryResponse(
        answer=answer,
        recommendations=recommendations[:5],  # Limit to 5 recommendations
        actions=actions[:3],  # Limit to 3 actions
    )


# WebSocket endpoint for streaming responses (skeleton for future implementation)
# @router.websocket("/stream")
# async def assistant_stream(
#     websocket: WebSocket,
#     session: SessionDep,
#     token: str = Query(...),
# ):
#     """
#     WebSocket endpoint for streaming AI assistant responses.
#     To be implemented in future iterations.
#     """
#     await websocket.accept()
#     # Implementation goes here
#     await websocket.close()
