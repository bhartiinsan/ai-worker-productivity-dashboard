@echo off
REM 🚀 AI Worker Productivity Dashboard - Windows One-Click Startup Script
REM This script starts the entire application with a single command

echo 🏭 Starting AI Worker Productivity Dashboard...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker is not running. Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Stop any existing containers
echo 🧹 Cleaning up existing containers...
docker compose down >nul 2>&1

REM Build and start containers
echo 🔨 Building containers (this may take a few minutes on first run^)...
docker compose up --build -d

REM Wait for backend to be healthy
echo.
echo ⏳ Waiting for backend to be ready...
set max_attempts=30
set attempt=0

:wait_loop
set /a attempt+=1
curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend is healthy!
    goto seed_db
)

if %attempt% geq %max_attempts% (
    echo ❌ Backend failed to start. Check logs with: docker compose logs backend
    pause
    exit /b 1
)

echo    Attempt %attempt%/%max_attempts%...
timeout /t 2 /nobreak >nul
goto wait_loop

:seed_db
REM Seed the database
echo.
echo 🌱 Seeding database with sample data...
curl -X POST "http://localhost:8000/api/admin/seed?clear_existing=true" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Database seeded successfully!
) else (
    echo ⚠️  Warning: Failed to seed database. You can do this manually later.
)

REM Final status
echo.
echo ═══════════════════════════════════════════════════════════
echo ✨ Application is running!
echo ═══════════════════════════════════════════════════════════
echo.
echo 📊 Dashboard:   http://localhost:3000
echo 🔧 API Docs:    http://localhost:8000/docs
echo ❤️  Health:      http://localhost:8000/health
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo To stop the application, run: docker compose down
echo To view logs, run: docker compose logs -f
echo.
pause
