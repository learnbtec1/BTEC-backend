from fastapi import APIRouter
from .endpoints import btec, assignments

api_router = APIRouter()

# ربط راوتر نقاط النهاية الخاصة بـ btec
api_router.include_router(btec.router, prefix="/btec", tags=["btec"])
# ربط راوتر نقاط النهاية الخاصة بـ assignments
api_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])