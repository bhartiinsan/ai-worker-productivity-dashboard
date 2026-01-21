param([ValidateSet('Setup', 'Start', 'StartDocker', 'Stop', 'StopAll', 'Test', 'Status', 'Clean', 'Help')][string]$Command = 'Help')
function Show-Banner {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " AI Worker Productivity Dashboard" -ForegroundColor Cyan
    Write-Host " Unified Workflow Manager" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}
function Show-Help {
    Show-Banner
    Write-Host "USAGE:" -ForegroundColor Green
    Write-Host "  .\manage.ps1 <Command>" -ForegroundColor White
    Write-Host ""
    Write-Host "COMMANDS:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Setup" -ForegroundColor Cyan
    Write-Host "    Initialize development environment" -ForegroundColor Gray
    Write-Host "    - Creates Python virtual environment" -ForegroundColor DarkGray
    Write-Host "    - Installs backend dependencies (FastAPI, SQLAlchemy, etc.)" -ForegroundColor DarkGray
    Write-Host "    - Installs frontend dependencies (React, TypeScript, etc.)" -ForegroundColor DarkGray
    Write-Host "    Usage: .\manage.ps1 Setup" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Start" -ForegroundColor Cyan
    Write-Host "    Launch backend (port 8000) and frontend (port 3000) locally" -ForegroundColor Gray
    Write-Host "    - Opens two PowerShell windows (backend + frontend)" -ForegroundColor DarkGray
    Write-Host "    - Auto-opens browser to http://localhost:3000" -ForegroundColor DarkGray
    Write-Host "    - Backend API docs: http://localhost:8000/docs" -ForegroundColor DarkGray
    Write-Host "    Usage: .\manage.ps1 Start" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  StartDocker" -ForegroundColor Cyan
    Write-Host "    Launch services using Docker Compose" -ForegroundColor Gray
    Write-Host "    - Requires Docker Desktop installed and running" -ForegroundColor DarkGray
    Write-Host "    - Builds images and starts containers in detached mode" -ForegroundColor DarkGray
    Write-Host "    - View logs: docker-compose logs -f" -ForegroundColor DarkGray
    Write-Host "    Usage: .\manage.ps1 StartDocker" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Stop" -ForegroundColor Cyan
    Write-Host "    Stop local Python and Node.js processes" -ForegroundColor Gray
    Write-Host "    - Kills all running python.exe and node.exe processes" -ForegroundColor DarkGray
    Write-Host "    - Does NOT stop Docker containers (use StopAll)" -ForegroundColor DarkGray
    Write-Host "    Usage: .\manage.ps1 Stop" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  StopAll" -ForegroundColor Cyan
    Write-Host "    Stop all services (local + Docker)" -ForegroundColor Gray
    Write-Host "    - Runs docker-compose down" -ForegroundColor DarkGray
    Write-Host "    - Stops local Python and Node.js processes" -ForegroundColor DarkGray
    Write-Host "    Usage: .\manage.ps1 StopAll" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Status" -ForegroundColor Cyan
    Write-Host "    Show which services are running" -ForegroundColor Gray
    Write-Host "    - Checks port 8000 (backend)" -ForegroundColor DarkGray
    Write-Host "    - Checks port 3000 (frontend)" -ForegroundColor DarkGray
    Write-Host "    Usage: .\manage.ps1 Status" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Test" -ForegroundColor Cyan
    Write-Host "    Verify project file structure" -ForegroundColor Gray
    Write-Host "    - Checks for required files (main.py, package.json, etc.)" -ForegroundColor DarkGray
    Write-Host "    Usage: .\manage.ps1 Test" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Clean" -ForegroundColor Cyan
    Write-Host "    Remove build artifacts and caches" -ForegroundColor Gray
    Write-Host "    - Deletes __pycache__ directories" -ForegroundColor DarkGray
    Write-Host "    - Removes frontend/build folder" -ForegroundColor DarkGray
    Write-Host "    - Deletes *.log files" -ForegroundColor DarkGray
    Write-Host "    Usage: .\manage.ps1 Clean" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  Help" -ForegroundColor Cyan
    Write-Host "    Display this help message" -ForegroundColor Gray
    Write-Host "    Usage: .\manage.ps1 Help" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "EXAMPLES:" -ForegroundColor Green
    Write-Host "  # First-time setup" -ForegroundColor Gray
    Write-Host "  .\manage.ps1 Setup" -ForegroundColor Yellow
    Write-Host "  .\manage.ps1 Start" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  # Check if services are running" -ForegroundColor Gray
    Write-Host "  .\manage.ps1 Status" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  # Restart services" -ForegroundColor Gray
    Write-Host "  .\manage.ps1 Stop" -ForegroundColor Yellow
    Write-Host "  .\manage.ps1 Start" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  # Docker deployment" -ForegroundColor Gray
    Write-Host "  .\manage.ps1 StartDocker" -ForegroundColor Yellow
    Write-Host "  docker-compose logs -f      # View logs" -ForegroundColor Yellow
    Write-Host "  .\manage.ps1 StopAll        # Stop containers" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "URLS:" -ForegroundColor Green
    Write-Host "  Frontend:    http://localhost:3000" -ForegroundColor Cyan
    Write-Host "  Backend:     http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  API Docs:    http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "  Redoc:       http://localhost:8000/redoc" -ForegroundColor Cyan
    Write-Host ""
}
function Initialize-Environment {
    Show-Banner
    Write-Host "[1/4] Python..." -ForegroundColor Yellow
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) { Write-Host "NOT FOUND" -ForegroundColor Red; return }
    Write-Host "OK" -ForegroundColor Green
    Write-Host "[2/4] venv..." -ForegroundColor Yellow
    if (-not (Test-Path "backend\.venv")) { python -m venv backend\.venv }
    Write-Host "OK" -ForegroundColor Green
    Write-Host "[3/4] pip install..." -ForegroundColor Yellow
    & "backend\.venv\Scripts\Activate.ps1"; pip install -q -r backend\requirements.txt
    Write-Host "OK" -ForegroundColor Green
    Write-Host "[4/4] npm install..." -ForegroundColor Yellow
    Push-Location frontend; npm install; Pop-Location
    Write-Host "OK" -ForegroundColor Green
    Write-Host "Setup complete!" -ForegroundColor Green
    Write-Host ""
}
function Start-Services {
    Show-Banner
    Write-Host "Starting backend..." -ForegroundColor Yellow
    $backendCmd = "cd backend; & .\.venv\Scripts\Activate.ps1; `$env:PYTHONPATH = (Get-Location).Path; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd -WindowStyle Normal
    Write-Host "OK" -ForegroundColor Green
    Start-Sleep -Seconds 3
    Write-Host "Starting frontend..." -ForegroundColor Yellow
    $frontendCmd = "cd frontend; npm start"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd -WindowStyle Normal
    Write-Host "OK" -ForegroundColor Green
    Write-Host ""
    Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host ""
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:3000"
}
function Start-DockerServices {
    Show-Banner
    Write-Host "Docker..." -ForegroundColor Yellow
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { Write-Host "NOT FOUND - Install Docker Desktop" -ForegroundColor Red; return }
    Write-Host "Building and starting..." -ForegroundColor Yellow
    docker-compose up -d --build
    Write-Host "OK" -ForegroundColor Green
    Write-Host ""
    Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "View logs: docker-compose logs -f" -ForegroundColor Gray
    Write-Host ""
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:3000"
}
function Stop-Services {
    Show-Banner
    Write-Host "Stopping..." -ForegroundColor Yellow
    Stop-Process -Name python, node -Force -ErrorAction SilentlyContinue
    Write-Host "OK" -ForegroundColor Green
    Write-Host ""
}
function Stop-AllServices {
    Show-Banner
    Write-Host "Stopping..." -ForegroundColor Yellow
    docker-compose down 2>&1 | Out-Null
    Stop-Process -Name python, node -Force -ErrorAction SilentlyContinue
    Write-Host "OK" -ForegroundColor Green
    Write-Host ""
}
function Get-ServiceStatus {
    Show-Banner
    Write-Host "Local Services:" -ForegroundColor Yellow
    if (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue) { Write-Host "  OK Backend" -ForegroundColor Green } else { Write-Host "  -- Backend" -ForegroundColor Yellow }
    if (Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue) { Write-Host "  OK Frontend" -ForegroundColor Green } else { Write-Host "  -- Frontend" -ForegroundColor Yellow }
    Write-Host ""
}
function Test-System {
    Show-Banner
    Write-Host "Files:" -ForegroundColor Yellow
    @("backend\app\main.py", "backend\requirements.txt", "frontend\package.json", "docker-compose.yml") | ForEach-Object { if (Test-Path $_) { Write-Host "  OK $_" -ForegroundColor Green } else { Write-Host "  !! $_" -ForegroundColor Red } }
    Write-Host ""
}
function Clean-Artifacts {
    Show-Banner
    Write-Host "Cleaning..." -ForegroundColor Yellow
    Get-ChildItem -Path backend -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item -Path $_.FullName -Recurse -Force -ErrorAction SilentlyContinue }
    if (Test-Path "frontend\build") { Remove-Item -Path "frontend\build" -Recurse -Force -ErrorAction SilentlyContinue }
    Get-ChildItem -Path . -Recurse -Filter "*.log" -ErrorAction SilentlyContinue | ForEach-Object { Remove-Item -Path $_.FullName -Force -ErrorAction SilentlyContinue }
    Write-Host "OK" -ForegroundColor Green
    Write-Host ""
}
switch ($Command.ToLower()) { 'setup' { Initialize-Environment } 'start' { Start-Services } 'startdocker' { Start-DockerServices } 'stop' { Stop-Services } 'stopall' { Stop-AllServices } 'test' { Test-System } 'status' { Get-ServiceStatus } 'clean' { Clean-Artifacts } 'help' { Show-Help } default { Show-Help } }
