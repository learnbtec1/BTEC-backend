@echo off
echo ===============================================
echo BTEC Assessment Engine - Backend Setup
echo ===============================================
echo.

cd backend

echo 1. Installing dependencies...
pip install -r requirements.txt
echo.

echo 2. Creating .env file...
if not exist .env (
    copy .env.example .env
    echo    Created .env file
) else (
    echo    .env already exists
)
echo.

echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo Next steps:
echo   1. Edit backend\.env and set your DATABASE_URL
echo   2. Run: cd backend
echo   3. Run: uvicorn app.main:app --host 0.0.0.0 --port 10000 --reload
echo.
pause
