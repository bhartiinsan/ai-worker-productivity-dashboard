# AI Worker Productivity Dashboard - Interactive Workflow Script
# Run with: .\workflow.ps1 -Setup | -Test | -Start | -Stop | -Clean | -Help

param(
    [switch]$Setup,
    [switch]$Test,
    [switch]$Start,
    [switch]$Stop,
    [switch]$Clean,
    [switch]$Help
)

function Show-Banner {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host " AI Worker Productivity Dashboard       " -ForegroundColor Cyan  
    Write-Host " Workflow Manager                        " -ForegroundColor Cyan
    Write-Host "=========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Help {
    Show-Banner
    Write-Host "USAGE: .\workflow.ps1 [OPTION]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "OPTIONS:" -ForegroundColor Green
    Write-Host "  -Setup    Setup environment (venv + dependencies)" -ForegroundColor White
    Write-Host "  -Test     Run system tests and health checks" -ForegroundColor White
    Write-Host "  -Start    Start backend and frontend services" -ForegroundColor White
    Write-Host "  -Stop     Stop all running services" -ForegroundColor White
    Write-Host "  -Clean    Clean all build artifacts" -ForegroundColor White
    Write-Host "  -Help     Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Green
    Write-Host "  .\workflow.ps1 -Setup     # First time setup" -ForegroundColor Cyan
    Write-Host "  .\workflow.ps1 -Test      # Verify everything works" -ForegroundColor Cyan
    Write-Host "  .\workflow.ps1 -Start     # Launch dashboard" -ForegroundColor Cyan
    Write-Host "" 
}

function Initialize-Environment {
    Show-Banner
    Write-Host "=== ENVIRONMENT SETUP ===" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "[1/4] Checking prerequisites..." -ForegroundColor Yellow
    
    $python = python --version 2>&1
    Write-Host "  Python: $python" -ForegroundColor Green
    
    $node = node --version 2>&1
    Write-Host "  Node.js: $node" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "[2/4] Setting up backend..." -ForegroundColor Yellow
    
    if (!(Test-Path "backend\.venv")) {
        Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
        python -m venv backend\.venv
    }
    
    Write-Host "  Installing Python dependencies..." -ForegroundColor Cyan
    & backend\.venv\Scripts\pip.exe install -r backend\requirements.txt --quiet
    Write-Host "  Backend dependencies installed" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "[3/4] Setting up frontend..." -ForegroundColor Yellow
    
    if (!(Test-Path "frontend\node_modules")) {
        Write-Host "  Installing Node dependencies..." -ForegroundColor Cyan
        Set-Location frontend
        npm install --silent
        Set-Location ..
    }
    Write-Host "  Frontend dependencies installed" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "[4/4] Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next: .\workflow.ps1 -Start" -ForegroundColor Cyan
    Write-Host ""
}

function Test-System {
    Show-Banner
    Write-Host "=== SYSTEM VERIFICATION ===" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "[Test 1] Checking files..." -ForegroundColor Yellow
    
    $files = @(
        "backend\app\main.py",
        "backend\requirements.txt",
        "frontend\package.json",
        "frontend\src\App.tsx"
    )
    
    foreach ($file in $files) {
        if (Test-Path $file) {
            Write-Host "  OK: $file" -ForegroundColor Green
        }
        else {
            Write-Host "  MISSING: $file" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "[Test 2] Checking services..." -ForegroundColor Yellow
    
    $backend = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if ($backend) {
        Write-Host "  Backend running on port 8000" -ForegroundColor Green
        
        $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($health.status -eq "healthy") {
            Write-Host "  Backend health: OK" -ForegroundColor Green
        }
    }
    else {
        Write-Host "  Backend not running" -ForegroundColor Yellow
    }
    
    $frontend = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
    if ($frontend) {
        Write-Host "  Frontend running on port 3000" -ForegroundColor Green
    }
    else {
        Write-Host "  Frontend not running" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "=== TESTS COMPLETE ===" -ForegroundColor Green
    Write-Host ""
}

function Start-Services {
    Show-Banner
    Write-Host "=== STARTING SERVICES ===" -ForegroundColor Green
    Write-Host ""
    Write-Host "System Architecture:" -ForegroundColor Yellow
    Write-Host "  Frontend (React + TypeScript) --> Port 3000" -ForegroundColor Cyan
    Write-Host "  Backend (FastAPI + Python)    --> Port 8000" -ForegroundColor Cyan
    Write-Host "  Database (SQLite)             --> productivity.db" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "[1/2] Starting backend..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\BACKEND.bat" -WindowStyle Minimized
    Start-Sleep -Seconds 5
    Write-Host "  Backend started" -ForegroundColor Green
    
    Write-Host "[2/2] Starting frontend..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\FRONTEND.bat" -WindowStyle Minimized
    Start-Sleep -Seconds 3
    Write-Host "  Frontend starting..." -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Waiting for services to initialize..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($health.status -eq "healthy") {
        Write-Host ""
        Write-Host "=========================================" -ForegroundColor Magenta
        Write-Host "   DASHBOARD IS READY!" -ForegroundColor Magenta
        Write-Host "=========================================" -ForegroundColor Magenta
        Write-Host ""
        Write-Host "Access URLs:" -ForegroundColor Yellow
        Write-Host "  Dashboard:   http://localhost:3000" -ForegroundColor Cyan
        Write-Host "  API Docs:    http://localhost:8000/docs" -ForegroundColor Cyan
        Write-Host "  Health:      http://localhost:8000/health" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Features to test:" -ForegroundColor Yellow
        Write-Host "  1. View real-time worker metrics" -ForegroundColor White
        Write-Host "  2. Toggle confidence filter" -ForegroundColor White
        Write-Host "  3. Click Reseed sample data" -ForegroundColor White
        Write-Host "  4. Watch auto-refresh (30s)" -ForegroundColor White
        Write-Host ""
        
        Start-Sleep -Seconds 3
        Write-Host "Opening browser..." -ForegroundColor Cyan
        Start-Process "http://localhost:3000"
    }
}

function Stop-Services {
    Show-Banner
    Write-Host "=== STOPPING SERVICES ===" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Stopping backend..." -ForegroundColor Yellow
    Stop-Process -Name python -Force -ErrorAction SilentlyContinue
    Write-Host "  Backend stopped" -ForegroundColor Green
    
    Write-Host "Stopping frontend..." -ForegroundColor Yellow
    Stop-Process -Name node -Force -ErrorAction SilentlyContinue
    Write-Host "  Frontend stopped" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "All services stopped!" -ForegroundColor Green
    Write-Host ""
}

function Clean-Artifacts {
    Show-Banner
    Write-Host "=== CLEANING BUILD ARTIFACTS ===" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "[1/3] Removing Python cache..." -ForegroundColor Yellow
    Get-ChildItem -Path backend -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
    Write-Host "  Python cache cleaned" -ForegroundColor Green
    
    Write-Host "[2/3] Removing frontend build..." -ForegroundColor Yellow
    if (Test-Path "frontend\build") {
        Remove-Item -Path "frontend\build" -Recurse -Force
        Write-Host "  Build removed" -ForegroundColor Green
    }
    
    Write-Host "[3/3] Cleaning logs..." -ForegroundColor Yellow
    Get-ChildItem -Path . -Recurse -Filter "*.log" -ErrorAction SilentlyContinue | Remove-Item -Force
    Write-Host "  Logs cleaned" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Cleanup complete!" -ForegroundColor Green
    Write-Host ""
}

# Main execution
if ($Help -or (!$Setup -and !$Test -and !$Start -and !$Stop -and !$Clean)) {
    Show-Help
    exit
}

if ($Setup) { Initialize-Environment }
if ($Test) { Test-System }
if ($Start) { Start-Services }
if ($Stop) { Stop-Services }
if ($Clean) { Clean-Artifacts }
