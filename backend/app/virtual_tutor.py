"""
Virtual Tutor Module

This module provides AI-powered recommendations for students based on their progress.
Analyzes performance across subjects and topics to suggest remediation strategies,
including AR simulation recommendations when appropriate.
"""

import uuid
from typing import Any

from sqlmodel import Session

from app import crud
from app.models import StudentProgress


def analyze_student_progress(
    *, session: Session, student_id: uuid.UUID
) -> dict[str, Any]:
    """
    Analyze student progress across all subjects and topics.

    Returns a dictionary containing:
    - weak_areas: List of subjects/topics where the student is struggling
    - strong_areas: List of subjects/topics where the student excels
    - overall_score: Average score across all progress entries
    - completion_rate: Percentage of completed topics
    """
    progress_list = crud.list_student_progress(
        session=session, student_id=student_id, skip=0, limit=1000
    )

    if not progress_list:
        return {
            "weak_areas": [],
            "strong_areas": [],
            "overall_score": 0.0,
            "completion_rate": 0.0,
            "total_topics": 0,
        }

    total_score = sum(p.score for p in progress_list)
    avg_score = total_score / len(progress_list)

    completed_count = sum(1 for p in progress_list if p.completed)
    completion_rate = (completed_count / len(progress_list)) * 100

    # Identify weak areas (score < 60)
    weak_areas = [
        {"subject": p.subject, "topic": p.topic, "score": p.score}
        for p in progress_list
        if p.score < 60.0
    ]

    # Identify strong areas (score >= 80)
    strong_areas = [
        {"subject": p.subject, "topic": p.topic, "score": p.score}
        for p in progress_list
        if p.score >= 80.0
    ]

    return {
        "weak_areas": weak_areas,
        "strong_areas": strong_areas,
        "overall_score": round(avg_score, 2),
        "completion_rate": round(completion_rate, 2),
        "total_topics": len(progress_list),
    }


def get_recommendations(
    *, session: Session, student_id: uuid.UUID
) -> dict[str, Any]:
    """
    Generate personalized recommendations for a student based on their progress.

    Includes:
    - Study recommendations for weak areas
    - AR simulation suggestions for hands-on practice
    - Motivational feedback based on strong areas
    - Overall learning path suggestions
    """
    analysis = analyze_student_progress(session=session, student_id=student_id)

    recommendations = {
        "analysis": analysis,
        "study_recommendations": [],
        "ar_simulations": [],
        "motivational_feedback": "",
    }

    # Generate study recommendations for weak areas
    for area in analysis["weak_areas"]:
        recommendations["study_recommendations"].append(
            {
                "subject": area["subject"],
                "topic": area["topic"],
                "priority": "high" if area["score"] < 40 else "medium",
                "suggestion": f"Focus on improving {area['topic']} in {area['subject']}. "
                f"Current score: {area['score']}%. "
                f"Recommended: Review core concepts and practice exercises.",
            }
        )

        # Suggest AR simulations for practical subjects
        if area["subject"].lower() in [
            "science",
            "engineering",
            "mathematics",
            "physics",
            "chemistry",
            "biology",
        ]:
            recommendations["ar_simulations"].append(
                {
                    "subject": area["subject"],
                    "topic": area["topic"],
                    "title": f"Interactive {area['topic']} Simulation",
                    "description": f"Hands-on AR experience to practice {area['topic']} concepts",
                    "ar_model_url": f"/ar/simulations/{area['subject'].lower()}/{area['topic'].lower().replace(' ', '-')}",
                    "difficulty": "beginner" if area["score"] < 40 else "intermediate",
                }
            )

    # Generate motivational feedback
    if analysis["overall_score"] >= 80:
        recommendations[
            "motivational_feedback"
        ] = "Excellent work! You're performing exceptionally well. Keep up the great effort!"
    elif analysis["overall_score"] >= 60:
        recommendations[
            "motivational_feedback"
        ] = "Good progress! Focus on your weak areas to improve further."
    else:
        recommendations[
            "motivational_feedback"
        ] = "Keep working hard! Consistent practice will help you improve. Don't give up!"

    # Add completion feedback
    if analysis["completion_rate"] < 50:
        recommendations["motivational_feedback"] += (
            f" Try to complete more topics - you're at {analysis['completion_rate']}% completion."
        )

    return recommendations
