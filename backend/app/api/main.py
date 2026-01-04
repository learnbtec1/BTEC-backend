from fastapi import APIRouter
from app.api.api_v1.api import api_router as v1_router

api_router = APIRouter()
# Include API v1 router under /api prefix
api_router.include_router(v1_router, prefix="/api")