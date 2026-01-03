from fastapi import APIRouter
from app.api.api_v1.api import api_router as v1_router

api_router = APIRouter()
# Include v1 router directly without additional prefix
api_router.include_router(v1_router)