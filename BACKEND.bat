@echo off
title Backend Server
cd /d "C:\Users\BHARTI\OneDrive\Desktop\Dashboard\backend"

echo ================================
echo   AI WORKER PRODUCTIVITY DASHBOARD
echo   Backend Server
echo ================================
echo.

REM Ensure database exists
set PYTHONPATH=%CD%
if not exist productivity.db (
    echo Creating database...
    .venv\Scripts\python.exe -c "from app.database import engine, Base; from app import models; Base.metadata.create_all(bind=engine)"
    echo Database created!
    echo.
)

echo Backend Server Running:
echo   - API: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

call .venv\Scripts\activate.bat
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
