from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import select

from app.api.deps import CurrentUser, SessionDep
from app.models_progress import StudentProgress

router = APIRouter()


class AssistantQuery(BaseModel):
    """Request model for assistant queries."""
    
    prompt: str
    context: str | None = None


class AssistantResponse(BaseModel):
    """Response model for assistant queries."""
    
    answer: str
    recommendations: list[str]
    actions: list[str]


@router.post("/query", response_model=AssistantResponse)
def query_assistant(
    query: AssistantQuery,
    session: SessionDep,
    current_user: CurrentUser,
) -> AssistantResponse:
    """
    Query the Keitagorus AI assistant.
    
    This is a mock implementation that provides deterministic responses
    based on keywords and user progress for demonstration purposes.
    
    Future implementation will integrate with actual AI models.
    
    WebSocket streaming endpoint: /api/v1/assistant/stream (TODO)
    """
    prompt_lower = query.prompt.lower()
    
    # Get user's progress to provide contextual recommendations
    statement = select(StudentProgress).where(
        StudentProgress.user_id == current_user.id
    )
    progress_records = session.exec(statement).all()
    
    struggling_count = sum(1 for p in progress_records if p.struggling)
    avg_score = (
        sum(p.last_score for p in progress_records if p.last_score is not None)
        / len([p for p in progress_records if p.last_score is not None])
        if any(p.last_score is not None for p in progress_records)
        else None
    )
    
    # Generate response based on keywords
    answer = ""
    recommendations = []
    actions = []
    
    if "help" in prompt_lower or "مساعدة" in prompt_lower:
        answer = "I'm Keitagorus (قيتاغورس), your AI learning assistant. I can help you with your BTEC coursework, provide study recommendations, and track your progress."
        recommendations = [
            "Review your recent lesson progress",
            "Practice more on topics where you scored below 70%",
            "Set daily study goals",
        ]
        actions = ["view_progress", "practice_exercises"]
    
    elif "progress" in prompt_lower or "تقدم" in prompt_lower:
        answer = f"You have {len(progress_records)} lesson(s) in progress."
        if struggling_count > 0:
            answer += f" I notice you're struggling with {struggling_count} lesson(s). Let me help!"
            recommendations = [
                "Focus on fundamentals before moving forward",
                "Try breaking down complex topics into smaller parts",
                "Schedule a review session for difficult topics",
            ]
        if avg_score is not None:
            answer += f" Your average score is {avg_score:.1f}%."
            if avg_score < 70:
                recommendations.append("Consider reviewing foundational concepts")
                actions.append("review_basics")
        actions.append("view_detailed_progress")
    
    elif "study" in prompt_lower or "دراسة" in prompt_lower:
        answer = "Here are personalized study recommendations based on your progress."
        recommendations = [
            "Create a study schedule with regular breaks",
            "Focus on active recall rather than passive reading",
            "Use spaced repetition for better retention",
        ]
        if struggling_count > 0:
            recommendations.insert(0, f"Prioritize the {struggling_count} topic(s) you're struggling with")
        actions = ["create_study_plan", "practice_mode"]
    
    elif "exam" in prompt_lower or "اختبار" in prompt_lower or "test" in prompt_lower:
        answer = "Let me help you prepare for your assessment."
        recommendations = [
            "Review all completed lessons",
            "Take practice tests to identify weak areas",
            "Create summary notes for each topic",
        ]
        actions = ["start_practice_test", "review_mistakes"]
    
    else:
        # Default response
        answer = f"I understand you're asking about: {query.prompt[:100]}..."
        if query.context:
            answer += f"\n\nBased on the context you provided, I suggest reviewing related materials."
        recommendations = [
            "Be more specific with your question",
            "Provide more context about what you're learning",
            "Try asking about specific topics or lessons",
        ]
        actions = ["refine_query"]
    
    # Add context-aware recommendations
    if query.context and "difficult" in query.context.lower():
        recommendations.insert(0, "Break down the problem into smaller steps")
        actions.append("step_by_step_guide")
    
    return AssistantResponse(
        answer=answer,
        recommendations=recommendations,
        actions=actions,
    )


# TODO: WebSocket endpoint for streaming responses
# @router.websocket("/stream")
# async def stream_assistant(websocket: WebSocket):
#     """
#     Stream assistant responses in real-time via WebSocket.
#     
#     This will be implemented in future iterations for better UX.
#     """
#     pass
