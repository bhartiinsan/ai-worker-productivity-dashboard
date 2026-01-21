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
    Write-Host "COMMANDS:" -ForegroundColor Green
    Write-Host "  Setup       - Initialize environment" -ForegroundColor White
    Write-Host "  Start       - Launch backend and frontend" -ForegroundColor White
    Write-Host "  StartDocker - Launch using Docker" -ForegroundColor White
    Write-Host "  Stop        - Stop local services" -ForegroundColor White
    Write-Host "  StopAll     - Stop all services" -ForegroundColor White
    Write-Host "  Test        - Run tests" -ForegroundColor White
    Write-Host "  Status      - Show status" -ForegroundColor White
    Write-Host "  Clean       - Clean artifacts" -ForegroundColor White
    Write-Host "  Help        - Show help" -ForegroundColor White
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
