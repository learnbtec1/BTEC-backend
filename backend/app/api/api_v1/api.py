from fastapi import APIRouter
from .endpoints import btec, tutor

api_router = APIRouter()

# ربط راوتر نقاط النهاية الخاصة بـ btec
api_router.include_router(btec.router, prefix="/btec", tags=["btec"])
api_router.include_router(tutor.router, prefix="/tutor", tags=["tutor"])