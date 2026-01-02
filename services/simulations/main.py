"""
Interactive Simulations Service
Virtual labs and realistic simulations
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import os

app = FastAPI(
    title="Interactive Simulations Service",
    description="Interactive Simulations - محاكاة تفاعلية",
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
class SimulationType(str, Enum):
    CHEMISTRY_LAB = "chemistry_lab"
    SURGERY = "surgery"
    SPACE = "space"
    ENGINEERING = "engineering"
    COURTROOM = "courtroom"
    PHYSICS_LAB = "physics_lab"
    BUSINESS = "business"

class Difficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

# Models
class Simulation(BaseModel):
    """Simulation definition"""
    id: str
    title: str
    description: str
    type: SimulationType
    difficulty: Difficulty
    vr_scene_url: str
    estimated_duration_minutes: int
    learning_objectives: List[str]
    prerequisites: List[str] = Field(default_factory=list)
    thumbnail_url: str
    max_participants: int = 1
    is_collaborative: bool = False

class ChemistryExperiment(BaseModel):
    """Chemistry lab experiment"""
    id: str
    name: str
    description: str
    chemicals_required: List[Dict[str, any]]
    equipment_required: List[str]
    procedure_steps: List[str]
    safety_warnings: List[str]
    expected_results: str
    difficulty: Difficulty

class SurgerySimulation(BaseModel):
    """Virtual surgery simulation"""
    id: str
    procedure_name: str
    description: str
    body_part: str
    difficulty: Difficulty
    steps: List[Dict[str, str]]
    instruments_required: List[str]
    complications: List[Dict[str, str]]
    success_criteria: List[str]
    duration_minutes: int

class SpaceSimulation(BaseModel):
    """Space exploration simulation"""
    id: str
    mission_name: str
    description: str
    destination: str
    spacecraft: str
    objectives: List[str]
    challenges: List[Dict[str, str]]
    duration_minutes: int
    difficulty: Difficulty

class EngineeringSimulation(BaseModel):
    """Engineering construction simulation"""
    id: str
    project_name: str
    description: str
    engineering_discipline: str  # civil, mechanical, electrical, etc.
    materials_required: List[Dict[str, any]]
    design_constraints: List[str]
    evaluation_criteria: List[str]
    difficulty: Difficulty

class CourtroomSimulation(BaseModel):
    """Virtual courtroom simulation"""
    id: str
    case_name: str
    description: str
    case_type: str  # criminal, civil, etc.
    roles: List[Dict[str, str]]
    evidence: List[Dict[str, any]]
    legal_concepts: List[str]
    duration_minutes: int
    difficulty: Difficulty

class SimulationSession(BaseModel):
    """Active simulation session"""
    session_id: str
    simulation_id: str
    user_id: str
    started_at: datetime
    status: str = Field(..., description="in_progress, completed, paused")
    progress_percentage: float = 0.0
    score: Optional[float] = None
    mistakes: int = 0
    hints_used: int = 0

class SimulationResult(BaseModel):
    """Simulation completion result"""
    session_id: str
    simulation_id: str
    user_id: str
    completed_at: datetime
    final_score: float = Field(..., ge=0, le=100)
    time_taken_minutes: int
    objectives_completed: List[str]
    mistakes_made: List[Dict[str, str]]
    performance_analysis: Dict[str, any]
    certificate_earned: bool = False

# Endpoints
@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "Interactive Simulations Service",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/v1/simulations", response_model=List[Simulation])
async def get_simulations(sim_type: Optional[SimulationType] = None):
    """Get all available simulations"""
    simulations = [
        Simulation(
            id="sim_chem_1",
            title="Acid-Base Titration",
            description="Learn precise titration techniques in a safe virtual environment",
            type=SimulationType.CHEMISTRY_LAB,
            difficulty=Difficulty.BEGINNER,
            vr_scene_url="/vr/simulations/chemistry/titration.glb",
            estimated_duration_minutes=30,
            learning_objectives=[
                "Understand acid-base reactions",
                "Master titration technique",
                "Calculate concentrations accurately"
            ],
            thumbnail_url="/thumbnails/chem_titration.jpg",
            max_participants=1
        ),
        Simulation(
            id="sim_surg_1",
            title="Appendectomy Procedure",
            description="Perform a virtual appendectomy with realistic anatomy",
            type=SimulationType.SURGERY,
            difficulty=Difficulty.ADVANCED,
            vr_scene_url="/vr/simulations/surgery/appendectomy.glb",
            estimated_duration_minutes=45,
            learning_objectives=[
                "Understand appendix anatomy",
                "Master surgical techniques",
                "Handle complications effectively"
            ],
            prerequisites=["Basic surgical anatomy", "Sterile techniques"],
            thumbnail_url="/thumbnails/surgery_appendectomy.jpg",
            max_participants=4,
            is_collaborative=True
        )
    ]
    
    if sim_type:
        simulations = [s for s in simulations if s.type == sim_type]
    
    return simulations

@app.get("/api/v1/chemistry-lab/{experiment_id}", response_model=ChemistryExperiment)
async def get_chemistry_experiment(experiment_id: str):
    """
    Get chemistry experiment details
    معمل الكيمياء الافتراضي
    """
    return ChemistryExperiment(
        id=experiment_id,
        name="Acid-Base Titration",
        description="Determine the concentration of an unknown acid using titration",
        chemicals_required=[
            {"name": "HCl (unknown concentration)", "amount": "50 mL"},
            {"name": "NaOH (0.1 M)", "amount": "burette"},
            {"name": "Phenolphthalein indicator", "amount": "2-3 drops"}
        ],
        equipment_required=[
            "Burette",
            "Pipette (25 mL)",
            "Erlenmeyer flask",
            "Beaker",
            "White tile"
        ],
        procedure_steps=[
            "Rinse burette with NaOH solution",
            "Fill burette with NaOH to zero mark",
            "Transfer 25 mL acid to flask using pipette",
            "Add 2-3 drops of phenolphthalein",
            "Titrate until permanent pink color",
            "Record volume used",
            "Calculate concentration"
        ],
        safety_warnings=[
            "Wear safety goggles",
            "Handle acids and bases with care",
            "Wipe up any spills immediately"
        ],
        expected_results="Pink endpoint indicates neutralization. Calculate acid concentration from volume of NaOH used.",
        difficulty=Difficulty.BEGINNER
    )

@app.get("/api/v1/surgery/{simulation_id}", response_model=SurgerySimulation)
async def get_surgery_simulation(simulation_id: str):
    """
    Get surgery simulation details
    مشرح الجراحة الافتراضي
    """
    return SurgerySimulation(
        id=simulation_id,
        procedure_name="Appendectomy",
        description="Laparoscopic removal of inflamed appendix",
        body_part="Appendix",
        difficulty=Difficulty.ADVANCED,
        steps=[
            {"step": 1, "description": "Make small incisions for laparoscopic ports"},
            {"step": 2, "description": "Insert camera and instruments"},
            {"step": 3, "description": "Identify appendix and mesoappendix"},
            {"step": 4, "description": "Clamp and cut mesoappendix"},
            {"step": 5, "description": "Ligate appendix base"},
            {"step": 6, "description": "Remove appendix through port"},
            {"step": 7, "description": "Check for bleeding and close incisions"}
        ],
        instruments_required=[
            "Laparoscope",
            "Graspers",
            "Scissors",
            "Clips",
            "Suction device"
        ],
        complications=[
            {"name": "Bleeding", "action": "Apply clips, cauterize"},
            {"name": "Perforation", "action": "Suction, irrigation, consider conversion"}
        ],
        success_criteria=[
            "Complete appendix removal",
            "No bleeding",
            "All ports closed properly",
            "Minimal tissue trauma"
        ],
        duration_minutes=45
    )

@app.get("/api/v1/space/{simulation_id}", response_model=SpaceSimulation)
async def get_space_simulation(simulation_id: str):
    """
    Get space simulation details
    محاكاة الفضاء
    """
    return SpaceSimulation(
        id=simulation_id,
        mission_name="Mars Landing Mission",
        description="Navigate a spacecraft to Mars and perform a successful landing",
        destination="Mars",
        spacecraft="Orbital Lander",
        objectives=[
            "Navigate to Mars orbit",
            "Calculate landing trajectory",
            "Perform atmospheric entry",
            "Execute powered descent",
            "Land safely on designated zone"
        ],
        challenges=[
            {"name": "Atmospheric entry", "difficulty": "high"},
            {"name": "Landing site selection", "difficulty": "medium"},
            {"name": "Fuel management", "difficulty": "high"}
        ],
        duration_minutes=60,
        difficulty=Difficulty.ADVANCED
    )

@app.post("/api/v1/start-simulation")
async def start_simulation(user_id: str, simulation_id: str):
    """Start a new simulation session"""
    session = SimulationSession(
        session_id=f"session_{datetime.utcnow().timestamp()}",
        simulation_id=simulation_id,
        user_id=user_id,
        started_at=datetime.utcnow(),
        status="in_progress"
    )
    return {
        "session": session,
        "message": "Simulation started successfully",
        "vr_url": f"/vr/simulation/{session.session_id}"
    }

@app.post("/api/v1/complete-simulation", response_model=SimulationResult)
async def complete_simulation(session_id: str, final_data: Dict[str, any]):
    """Complete a simulation and get results"""
    return SimulationResult(
        session_id=session_id,
        simulation_id=final_data.get("simulation_id", ""),
        user_id=final_data.get("user_id", ""),
        completed_at=datetime.utcnow(),
        final_score=85.5,
        time_taken_minutes=42,
        objectives_completed=[
            "Completed all procedure steps",
            "Followed safety protocols",
            "Achieved desired results"
        ],
        mistakes_made=[
            {"step": "Step 3", "description": "Minor deviation from optimal technique"}
        ],
        performance_analysis={
            "accuracy": 88.0,
            "speed": 82.0,
            "safety": 95.0,
            "technique": 85.0
        },
        certificate_earned=True
    )

@app.get("/api/v1/leaderboard/{simulation_id}")
async def get_simulation_leaderboard(simulation_id: str, limit: int = 10):
    """Get top performers for a simulation"""
    return {
        "simulation_id": simulation_id,
        "leaderboard": [
            {
                "rank": 1,
                "user_id": "user_1",
                "name": "Sarah Ahmed",
                "score": 98.5,
                "time_minutes": 35
            },
            {
                "rank": 2,
                "user_id": "user_2",
                "name": "Mohammed Ali",
                "score": 96.2,
                "time_minutes": 38
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8006))
    uvicorn.run(app, host="0.0.0.0", port=port)
