from fastapi import APIRouter
from .endpoints import btec
from app.btec_activation.router import router as activation_router

api_router = APIRouter()

# ربط راوتر نقاط النهاية الخاصة بـ btec
api_router.include_router(btec.router, prefix="/btec", tags=["btec"])
# ربط راوتر نظام مفاتيح التفعيل
api_router.include_router(activation_router)