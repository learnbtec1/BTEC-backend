from fastapi import APIRouter
from .endpoints import btec, files, login

api_router = APIRouter()

# ربط راوتر نقاط النهاية الخاصة بـ btec
api_router.include_router(btec.router, prefix="/btec", tags=["btec"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(files.router, prefix="/files", tags=["files"])