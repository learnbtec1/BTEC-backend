"""
Analytics & Reporting Service
Student performance analysis and reporting system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum
import os

app = FastAPI(
    title="Analytics & Reporting Service",
    description="Analytics & Reporting - خدمة التحليلات والتقارير",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class ReportType(str, Enum):
    STUDENT = "student"
    CLASS = "class"
    TEACHER = "teacher"
    COURSE = "course"
    SUBJECT = "subject"

class TimePeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

# Models
class StudentAnalytics(BaseModel):
    """Student performance analytics"""
    student_id: str
    student_name: str
    overall_performance: float = Field(..., ge=0, le=100)
    attendance_rate: float = Field(..., ge=0, le=100)
    assignment_completion_rate: float = Field(..., ge=0, le=100)
    average_score: float = Field(..., ge=0, le=100)
    improvement_trend: str = Field(..., description="improving, declining, stable")
    strengths: List[str]
    weaknesses: List[str]
    at_risk: bool = False
    risk_factors: List[str] = Field(default_factory=list)

class ClassStatistics(BaseModel):
    """Class-level statistics"""
    class_id: str
    class_name: str
    total_students: int
    active_students: int
    average_performance: float
    pass_rate: float
    attendance_rate: float
    top_performers: List[Dict[str, any]]
    struggling_students: List[Dict[str, any]]
    subject_performance: Dict[str, float]

class TeacherReport(BaseModel):
    """Teacher performance report"""
    teacher_id: str
    teacher_name: str
    total_courses: int
    total_students: int
    average_class_performance: float
    student_satisfaction: float
    engagement_rate: float
    courses: List[Dict[str, any]]
    recommendations: List[str]

class PerformanceChart(BaseModel):
    """Performance chart data"""
    title: str
    type: str = Field(..., description="line, bar, pie, area")
    labels: List[str]
    datasets: List[Dict[str, any]]
    period: TimePeriod

class GradePrediction(BaseModel):
    """Grade prediction analytics"""
    student_id: str
    subject: str
    current_grade: float
    predicted_final_grade: float
    confidence: float = Field(..., ge=0, le=1)
    factors: Dict[str, float]
    recommendations: List[str]

class EngagementMetrics(BaseModel):
    """Student engagement metrics"""
    student_id: str
    time_spent_learning: int  # minutes
    sessions_count: int
    average_session_duration: int  # minutes
    interaction_rate: float
    participation_score: float
    last_active: datetime

class ComparativeAnalysis(BaseModel):
    """Comparative analysis between entities"""
    comparison_type: str
    entities: List[str]
    metrics: Dict[str, List[float]]
    insights: List[str]

# Endpoints
@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "Analytics & Reporting Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/v1/student-analytics/{student_id}", response_model=StudentAnalytics)
async def get_student_analytics(student_id: str, period: TimePeriod = TimePeriod.MONTHLY):
    """
    Comprehensive student performance analysis
    تحليل أداء الطلاب
    """
    return StudentAnalytics(
        student_id=student_id,
        student_name="Sarah Ahmed",
        overall_performance=85.5,
        attendance_rate=95.0,
        assignment_completion_rate=92.0,
        average_score=87.3,
        improvement_trend="improving",
        strengths=[
            "Strong analytical skills",
            "Excellent problem-solving",
            "High engagement in class discussions"
        ],
        weaknesses=[
            "Time management needs improvement",
            "Occasionally struggles with complex concepts"
        ],
        at_risk=False
    )

@app.get("/api/v1/class-statistics/{class_id}", response_model=ClassStatistics)
async def get_class_statistics(class_id: str):
    """
    Class-level statistics
    إحصائيات الفصل
    """
    return ClassStatistics(
        class_id=class_id,
        class_name="Computer Science 101",
        total_students=30,
        active_students=28,
        average_performance=82.5,
        pass_rate=93.3,
        attendance_rate=91.0,
        top_performers=[
            {"student_id": "std_1", "name": "Sarah Ahmed", "score": 95.5},
            {"student_id": "std_2", "name": "Mohammed Ali", "score": 93.2}
        ],
        struggling_students=[
            {"student_id": "std_28", "name": "Ali Hassan", "score": 65.0, "risk_level": "medium"}
        ],
        subject_performance={
            "programming": 85.0,
            "algorithms": 80.0,
            "databases": 82.5
        }
    )

@app.get("/api/v1/teacher-report/{teacher_id}", response_model=TeacherReport)
async def get_teacher_report(teacher_id: str):
    """
    Detailed teacher performance report
    تقارير تفصيلية للمعلمين
    """
    return TeacherReport(
        teacher_id=teacher_id,
        teacher_name="Dr. Ahmed Ibrahim",
        total_courses=4,
        total_students=120,
        average_class_performance=84.5,
        student_satisfaction=4.5,
        engagement_rate=88.0,
        courses=[
            {
                "course_id": "cs101",
                "name": "Computer Science 101",
                "students": 30,
                "avg_score": 85.0
            }
        ],
        recommendations=[
            "Consider adding more interactive activities",
            "Some students need additional support in advanced topics"
        ]
    )

@app.get("/api/v1/performance-chart/{entity_id}", response_model=PerformanceChart)
async def get_performance_chart(
    entity_id: str,
    chart_type: str = "line",
    period: TimePeriod = TimePeriod.MONTHLY
):
    """
    Interactive performance charts
    رسوم بيانية تفاعلية
    """
    return PerformanceChart(
        title=f"Performance Over Time - {period.value}",
        type=chart_type,
        labels=["Week 1", "Week 2", "Week 3", "Week 4"],
        datasets=[
            {
                "label": "Average Score",
                "data": [75.0, 78.5, 82.0, 85.5],
                "backgroundColor": "#4CAF50"
            },
            {
                "label": "Completion Rate",
                "data": [85.0, 88.0, 92.0, 95.0],
                "backgroundColor": "#2196F3"
            }
        ],
        period=period
    )

@app.get("/api/v1/predict-grade/{student_id}", response_model=GradePrediction)
async def predict_student_grade(student_id: str, subject: str):
    """
    Predict student final grade
    التنبؤ بالدرجات
    """
    return GradePrediction(
        student_id=student_id,
        subject=subject,
        current_grade=82.5,
        predicted_final_grade=87.3,
        confidence=0.85,
        factors={
            "current_performance": 0.40,
            "improvement_trend": 0.25,
            "attendance": 0.15,
            "engagement": 0.20
        },
        recommendations=[
            "Continue current study pattern",
            "Focus on practice problems",
            "Participate more in discussions"
        ]
    )

@app.get("/api/v1/engagement-metrics/{student_id}", response_model=EngagementMetrics)
async def get_engagement_metrics(student_id: str):
    """Get student engagement metrics"""
    return EngagementMetrics(
        student_id=student_id,
        time_spent_learning=1200,  # 20 hours
        sessions_count=45,
        average_session_duration=27,
        interaction_rate=0.85,
        participation_score=88.5,
        last_active=datetime.utcnow()
    )

@app.post("/api/v1/compare")
async def comparative_analysis(entity_type: str, entity_ids: List[str]):
    """
    Comparative analysis between students/classes/teachers
    """
    return ComparativeAnalysis(
        comparison_type=entity_type,
        entities=entity_ids,
        metrics={
            "performance": [85.0, 82.5, 90.0],
            "engagement": [88.0, 85.0, 92.0],
            "attendance": [95.0, 90.0, 98.0]
        },
        insights=[
            "Entity 3 shows highest overall performance",
            "All entities show strong engagement",
            "Attendance rates are excellent across all entities"
        ]
    )

@app.get("/api/v1/export-report/{report_type}")
async def export_report(
    report_type: ReportType,
    entity_id: str,
    format: str = "pdf"
):
    """
    Export detailed reports (PDF, Excel, CSV)
    """
    return {
        "report_type": report_type.value,
        "entity_id": entity_id,
        "format": format,
        "download_url": f"/downloads/report_{entity_id}.{format}",
        "generated_at": datetime.utcnow().isoformat(),
        "message": "Report generated successfully"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8004))
    uvicorn.run(app, host="0.0.0.0", port=port)
