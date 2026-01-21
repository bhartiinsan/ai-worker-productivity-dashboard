@echo off
cls
echo.
echo ===============================================
echo   DOCKER ONE-COMMAND SETUP
echo   AI Worker Productivity Dashboard
echo ===============================================
echo.

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed or not running
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo [1/5] Docker detected
docker --version
echo.

REM Check Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose not found
    pause
    exit /b 1
)

echo [2/5] Docker Compose detected
docker-compose --version
echo.

REM Stop existing containers
echo [3/5] Stopping existing containers...
docker-compose down >nul 2>&1
echo   Stopped
echo.

REM Build and start
echo [4/5] Building and starting services...
echo   This may take 2-3 minutes on first run...
echo.
docker-compose up -d --build

if errorlevel 1 (
    echo.
    echo [ERROR] Docker Compose failed
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo [5/5] Waiting for services to be healthy...
timeout /t 15 /nobreak >nul

REM Seed database
echo.
echo Seeding database with sample data...
timeout /t 5 /nobreak >nul
curl -X POST "http://localhost:8000/api/seed?clear_existing=true&hours_back=24" --silent >nul 2>&1

if not errorlevel 1 (
    echo   Database seeded successfully!
) else (
    echo   Database will seed on first UI load
)

REM Success
echo.
echo ===============================================
echo   DASHBOARD IS READY!
echo ===============================================
echo.
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo.
echo   Docker Containers:
docker-compose ps
echo.
echo   To view logs: docker-compose logs -f
echo   To stop:      docker-compose down
echo.

echo Opening dashboard in browser...
timeout /t 2 /nobreak >nul
start http://localhost:3000

echo.
echo ===============================================
pause
