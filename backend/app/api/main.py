from fastapi import APIRouter
from app.api.api_v1.api import api_router as v1_router

api_router = APIRouter()
# نضم راوتر الإصدار 1 تحت بادئة /api
api_router.include_router(v1_router)