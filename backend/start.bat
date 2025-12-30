@echo off
echo Starting BTEC Assessment Engine Backend...
echo.

cd backend
uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
