"""
Virtual Campus Service
VR/AR enabled virtual campus with classrooms and labs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import os

app = FastAPI(
    title="Virtual Campus Service",
    description="Virtual Campus - حرم جامعي افتراضي كامل",
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
class RoomType(str, Enum):
    CLASSROOM = "classroom"
    LAB = "lab"
    LIBRARY = "library"
    AUDITORIUM = "auditorium"
    COLLABORATION_SPACE = "collaboration_space"
    HISTORICAL_WORLD = "historical_world"
    SCIENTIFIC_WORLD = "scientific_world"

class LabType(str, Enum):
    CHEMISTRY = "chemistry"
    PHYSICS = "physics"
    PROGRAMMING = "programming"
    BIOLOGY = "biology"
    ENGINEERING = "engineering"

# Models
class VirtualRoom(BaseModel):
    """Virtual room/space"""
    id: str
    name: str
    type: RoomType
    description: str
    capacity: int
    vr_scene_url: str
    thumbnail_url: str
    is_active: bool = True
    features: List[str]
    current_occupancy: int = 0

class VirtualClassroom(BaseModel):
    """Smart interactive classroom"""
    id: str
    name: str
    description: str
    capacity: int
    vr_scene_url: str
    teacher_id: Optional[str] = None
    course_id: Optional[str] = None
    features: List[str] = Field(
        default_factory=lambda: [
            "Interactive whiteboard",
            "3D visualizations",
            "Real-time collaboration",
            "Screen sharing",
            "Breakout rooms"
        ]
    )
    is_live: bool = False
    current_participants: int = 0

class VirtualLab(BaseModel):
    """Virtual laboratory"""
    id: str
    name: str
    type: LabType
    description: str
    vr_scene_url: str
    experiments: List[Dict[str, any]]
    equipment: List[Dict[str, str]]
    safety_protocols: List[str]
    max_users: int

class SmartLibrary(BaseModel):
    """Smart digital library"""
    id: str
    name: str
    description: str
    vr_scene_url: str
    total_books: int
    digital_books: int
    interactive_books: int
    categories: List[str]
    features: List[str] = Field(
        default_factory=lambda: [
            "3D book browsing",
            "AI research assistant",
            "Interactive reading",
            "Note-taking system",
            "Citation generator"
        ]
    )

class LectureTheater(BaseModel):
    """Virtual lecture theater"""
    id: str
    name: str
    capacity: int
    vr_scene_url: str
    is_live: bool = False
    scheduled_lectures: List[Dict[str, any]]
    features: List[str] = Field(
        default_factory=lambda: [
            "360-degree video",
            "Live Q&A",
            "Interactive polls",
            "Recording capability",
            "Multi-language subtitles"
        ]
    )

class CollaborationZone(BaseModel):
    """Collaboration space for teamwork"""
    id: str
    name: str
    description: str
    vr_scene_url: str
    max_participants: int
    tools: List[str] = Field(
        default_factory=lambda: [
            "Shared whiteboard",
            "3D modeling space",
            "Document collaboration",
            "Video conferencing",
            "Project management"
        ]
    )
    active_sessions: int = 0

class HistoricalWorld(BaseModel):
    """Historical world for exploration"""
    id: str
    name: str
    era: str
    civilization: str
    description: str
    vr_scene_url: str
    landmarks: List[Dict[str, str]]
    guided_tour_available: bool = True
    educational_content: List[Dict[str, any]]

class ScientificWorld(BaseModel):
    """Scientific exploration world"""
    id: str
    name: str
    category: str  # space, human_body, microscopic, etc.
    description: str
    vr_scene_url: str
    interactive_elements: List[Dict[str, any]]
    learning_objectives: List[str]

class CampusSession(BaseModel):
    """Active campus session"""
    session_id: str
    user_id: str
    room_id: str
    room_type: RoomType
    joined_at: datetime
    is_active: bool = True

# Endpoints
@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "Virtual Campus Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/v1/classrooms", response_model=List[VirtualClassroom])
async def get_classrooms(active_only: bool = False):
    """
    Get all virtual classrooms
    الفصول الذكية التفاعلية
    """
    return [
        VirtualClassroom(
            id="class_1",
            name="Main Lecture Hall",
            description="Primary virtual classroom for large lectures",
            capacity=100,
            vr_scene_url="/vr/scenes/classroom_main.glb",
            is_live=True,
            current_participants=45
        )
    ]

@app.get("/api/v1/labs", response_model=List[VirtualLab])
async def get_virtual_labs(lab_type: Optional[LabType] = None):
    """
    Get virtual laboratories
    المعامل الافتراضية
    """
    return [
        VirtualLab(
            id="lab_chem_1",
            name="Chemistry Lab - Organic",
            type=LabType.CHEMISTRY,
            description="Virtual chemistry lab for organic chemistry experiments",
            vr_scene_url="/vr/scenes/lab_chemistry.glb",
            experiments=[
                {
                    "id": "exp_1",
                    "name": "Titration",
                    "difficulty": "beginner",
                    "duration_minutes": 30
                }
            ],
            equipment=[
                {"name": "Beaker", "quantity": "10"},
                {"name": "Burette", "quantity": "5"},
                {"name": "Flask", "quantity": "8"}
            ],
            safety_protocols=[
                "Wear virtual safety goggles",
                "Handle chemicals with care",
                "Follow disposal procedures"
            ],
            max_users=20
        )
    ]

@app.get("/api/v1/library", response_model=SmartLibrary)
async def get_smart_library():
    """
    Get smart library information
    المكتبة الذكية
    """
    return SmartLibrary(
        id="lib_main",
        name="MetaLearn Central Library",
        description="Comprehensive digital library with interactive books",
        vr_scene_url="/vr/scenes/library_main.glb",
        total_books=50000,
        digital_books=45000,
        interactive_books=5000,
        categories=[
            "Science & Technology",
            "Mathematics",
            "Literature",
            "History",
            "Arts",
            "Medicine"
        ]
    )

@app.get("/api/v1/lecture-theaters", response_model=List[LectureTheater])
async def get_lecture_theaters():
    """
    Get lecture theaters
    مسارح المحاضرات
    """
    return [
        LectureTheater(
            id="theater_1",
            name="Grand Auditorium",
            capacity=500,
            vr_scene_url="/vr/scenes/auditorium_grand.glb",
            is_live=False,
            scheduled_lectures=[
                {
                    "id": "lec_1",
                    "title": "Introduction to AI",
                    "lecturer": "Dr. Sarah Ahmed",
                    "time": "2024-01-15T14:00:00Z"
                }
            ]
        )
    ]

@app.get("/api/v1/collaboration-zones", response_model=List[CollaborationZone])
async def get_collaboration_zones():
    """
    Get collaboration spaces
    مناطق التعاون
    """
    return [
        CollaborationZone(
            id="collab_1",
            name="Innovation Hub",
            description="Creative space for team projects",
            vr_scene_url="/vr/scenes/collab_hub.glb",
            max_participants=12,
            active_sessions=3
        )
    ]

@app.get("/api/v1/historical-worlds", response_model=List[HistoricalWorld])
async def get_historical_worlds():
    """
    Get historical exploration worlds
    العوالم التاريخية
    """
    return [
        HistoricalWorld(
            id="hist_egypt",
            name="Ancient Egypt",
            era="Ancient",
            civilization="Egyptian",
            description="Explore ancient Egyptian pyramids and temples",
            vr_scene_url="/vr/scenes/ancient_egypt.glb",
            landmarks=[
                {"name": "Great Pyramid of Giza", "coordinates": "29.9792,31.1342"},
                {"name": "Sphinx", "coordinates": "29.9753,31.1376"}
            ],
            guided_tour_available=True,
            educational_content=[
                {"title": "Pyramid Construction", "type": "video", "duration": 15},
                {"title": "Hieroglyphics Guide", "type": "interactive", "duration": 20}
            ]
        )
    ]

@app.get("/api/v1/scientific-worlds", response_model=List[ScientificWorld])
async def get_scientific_worlds():
    """
    Get scientific exploration worlds
    العوالم العلمية
    """
    return [
        ScientificWorld(
            id="sci_space",
            name="Solar System Tour",
            category="space",
            description="Journey through our solar system",
            vr_scene_url="/vr/scenes/solar_system.glb",
            interactive_elements=[
                {"type": "planet", "name": "Mars", "interactions": ["explore_surface", "view_info"]},
                {"type": "moon", "name": "Europa", "interactions": ["analyze_ice"]}
            ],
            learning_objectives=[
                "Understand planetary motion",
                "Learn about celestial bodies",
                "Explore space phenomena"
            ]
        ),
        ScientificWorld(
            id="sci_body",
            name="Human Body Journey",
            category="human_body",
            description="Explore the human body from inside",
            vr_scene_url="/vr/scenes/human_body.glb",
            interactive_elements=[
                {"type": "organ", "name": "Heart", "interactions": ["view_structure", "simulate_function"]},
                {"type": "system", "name": "Circulatory", "interactions": ["follow_blood_flow"]}
            ],
            learning_objectives=[
                "Understand organ functions",
                "Learn body systems",
                "Visualize biological processes"
            ]
        )
    ]

@app.post("/api/v1/join-room")
async def join_virtual_room(user_id: str, room_id: str, room_type: RoomType):
    """Join a virtual room"""
    session = CampusSession(
        session_id=f"session_{datetime.utcnow().timestamp()}",
        user_id=user_id,
        room_id=room_id,
        room_type=room_type,
        joined_at=datetime.utcnow()
    )
    return {
        "session": session,
        "message": "Successfully joined virtual room",
        "vr_connection_url": f"/vr/connect/{session.session_id}"
    }

@app.post("/api/v1/leave-room")
async def leave_virtual_room(session_id: str):
    """Leave a virtual room"""
    return {
        "session_id": session_id,
        "message": "Successfully left virtual room",
        "duration_minutes": 45
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8005))
    uvicorn.run(app, host="0.0.0.0", port=port)
