@echo off
cls
echo.
echo ===============================================
echo   AI WORKER PRODUCTIVITY DASHBOARD
echo   Complete Setup and Launch
echo ===============================================
echo.

cd /d "%~dp0"

REM Step 1: Check Prerequisites
echo [1/5] Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install from https://python.org
    pause
    exit /b 1
)
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found. Install from https://nodejs.org
    pause
    exit /b 1
)
echo   Python: OK
echo   Node.js: OK
echo.

REM Step 2: Setup Backend
echo [2/5] Setting up Python backend...
cd backend

if not exist .venv (
    echo   Creating virtual environment...
    python -m venv .venv
)

echo   Installing Python packages...
call .venv\Scripts\activate.bat
python -m pip install --quiet --upgrade pip >nul 2>&1
pip install --quiet -r requirements.txt

echo   Creating database...
set PYTHONPATH=%CD%
.venv\Scripts\python.exe -c "from app.database import engine, Base; from app import models; Base.metadata.create_all(bind=engine)" >nul 2>&1

cd ..
echo   Backend setup complete!
echo.

REM Step 3: Setup Frontend
echo [3/5] Checking frontend dependencies...
cd frontend

if not exist node_modules (
    echo   Installing Node.js packages (this may take 2-3 minutes)...
    call npm install --silent
) else (
    echo   Node modules already installed
)

cd ..
echo   Frontend setup complete!
echo.

REM Step 4: Start Servers
echo [4/5] Starting servers...
echo.
echo   Starting Backend Server (Port 8000)...
start "🔌 Backend API - Port 8000" cmd /k "cd /d %CD%\backend && call .venv\Scripts\activate.bat && echo ================================ && echo   BACKEND SERVER RUNNING && echo ================================ && echo. && echo   API: http://localhost:8000 && echo   Docs: http://localhost:8000/docs && echo. && echo   Press Ctrl+C to stop && echo. && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo   Waiting for backend to start...
timeout /t 10 /nobreak >nul

echo   Starting Frontend Server (Port 3000)...
start "🌐 Frontend Dashboard - Port 3000" cmd /k "cd /d %CD%\frontend && set BROWSER=none && echo ================================ && echo   FRONTEND SERVER RUNNING && echo ================================ && echo. && echo   Dashboard: http://localhost:3000 && echo. && echo   Press Ctrl+C to stop && echo. && npm start"

echo   Waiting for frontend to compile...
timeout /t 12 /nobreak >nul

REM Step 5: Seed Database
echo.
echo [5/5] Seeding database with sample data...
timeout /t 3 /nobreak >nul

curl -X POST "http://localhost:8000/api/seed?clear_existing=true&hours_back=24" --silent >nul 2>&1
if not errorlevel 1 (
    echo   Database seeded: 6 workers, 6 workstations, 24h of events
) else (
    echo   Seeding will happen on first dashboard load
)

REM Success Message
echo.
echo ===============================================
echo   DASHBOARD IS READY!
echo ===============================================
echo.
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo.
echo   New Features:
echo   - Auto-refresh every 30 seconds
echo   - Model health monitoring
echo   - Efficiency heatmap
echo.
echo   Both servers are running in separate windows
echo   Close those windows to stop the services
echo.

REM Open Browser
echo Opening dashboard in browser...
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo ===============================================
echo   ENJOY YOUR DASHBOARD! 
echo ===============================================
echo.
pause
