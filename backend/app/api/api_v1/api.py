from fastapi import APIRouter
from .endpoints import assistant, btec, files, login

api_router = APIRouter()

# Include routers for all endpoints
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["assistant"])
api_router.include_router(btec.router, prefix="/btec", tags=["btec"])