# 🖥️ CLI Reference - Workflow Manager

Complete command-line reference for the `manage.ps1` PowerShell workflow manager.

---

## Quick Start

```powershell
# First-time setup
.\manage.ps1 Setup

# Launch services
.\manage.ps1 Start

# Check status
.\manage.ps1 Status
```

---

## Command Reference

### `Setup` - Initialize Environment

**Purpose**: Prepare development environment for first run

**Actions**:
1. ✅ Verify Python installation
2. 📦 Create Python virtual environment (`backend\.venv`)
3. 📥 Install backend dependencies from `requirements.txt`
4. 📥 Install frontend dependencies from `package.json`

**Usage**:
```powershell
.\manage.ps1 Setup
```

**Output**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

[1/4] Python...
OK
[2/4] venv...
OK
[3/4] pip install...
OK
[4/4] npm install...
OK
Setup complete!
```

**When to Use**:
- First time cloning the repository
- After pulling major dependency changes
- When switching Python versions
- To reset virtual environment

---

### `Start` - Launch Local Services

**Purpose**: Start backend (FastAPI) and frontend (React) in development mode

**Actions**:
1. 🐍 Start backend on `http://localhost:8000`
   - Activates Python virtual environment
   - Sets `PYTHONPATH` to backend directory
   - Runs `uvicorn app.main:app --reload`
   - Opens in new PowerShell window

2. ⚛️ Start frontend on `http://localhost:3000`
   - Runs `npm start`
   - Opens in new PowerShell window
   - Auto-opens browser to dashboard

**Usage**:
```powershell
.\manage.ps1 Start
```

**Output**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

Starting backend...
OK
Starting frontend...
OK

Backend:  http://localhost:8000
Frontend: http://localhost:3000
API Docs: http://localhost:8000/docs
```

**Process Management**:
- Backend window: Keep open for live reload
- Frontend window: Shows webpack dev server logs
- Close windows manually or use `.\manage.ps1 Stop`

**Troubleshooting**:
```powershell
# If ports already in use
.\manage.ps1 Stop
.\manage.ps1 Start

# Or kill specific processes
Get-NetTCPConnection -LocalPort 8000,3000 | ForEach-Object { 
    Stop-Process -Id $_.OwningProcess -Force 
}
```

---

### `StartDocker` - Launch with Docker

**Purpose**: Run services in Docker containers (production-like environment)

**Prerequisites**:
- Docker Desktop installed and running
- WSL 2 backend enabled (Windows)

**Actions**:
1. 🐳 Verify Docker availability
2. 🏗️ Build Docker images (backend + frontend)
3. 🚀 Start containers in detached mode
4. 🌐 Auto-open browser to `http://localhost:3000`

**Usage**:
```powershell
.\manage.ps1 StartDocker
```

**Output**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

Docker...
Building and starting...
[+] Building 45.2s (24/24) FINISHED
[+] Running 2/2
 ✔ Container ai-worker-backend  Started
 ✔ Container ai-worker-frontend Started
OK

Backend:  http://localhost:8000
Frontend: http://localhost:3000

View logs: docker-compose logs -f
```

**Container Management**:
```powershell
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart containers
docker-compose restart

# Stop containers
.\manage.ps1 StopAll
```

**Production Notes**:
- Uses Nginx for frontend serving
- PostgreSQL instead of SQLite (configure in docker-compose.yml)
- Environment variables from `.env` file

---

### `Stop` - Stop Local Services

**Purpose**: Terminate local Python and Node.js processes

**Actions**:
- Kills all `python.exe` processes
- Kills all `node.exe` processes
- Does NOT stop Docker containers

**Usage**:
```powershell
.\manage.ps1 Stop
```

**Output**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

Stopping...
OK
```

**Warning**: This stops ALL Python/Node processes, not just this project. Use with caution if running other Python/Node services.

---

### `StopAll` - Stop All Services

**Purpose**: Stop both local services AND Docker containers

**Actions**:
1. 🐳 Run `docker-compose down`
2. 🛑 Kill local Python processes
3. 🛑 Kill local Node.js processes

**Usage**:
```powershell
.\manage.ps1 StopAll
```

**Output**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

Stopping...
[+] Running 3/3
 ✔ Container ai-worker-frontend  Removed
 ✔ Container ai-worker-backend   Removed
 ✔ Network ai-worker-network     Removed
OK
```

---

### `Status` - Check Running Services

**Purpose**: Show which services are currently active

**Actions**:
- Checks if port 8000 is listening (backend)
- Checks if port 3000 is listening (frontend)

**Usage**:
```powershell
.\manage.ps1 Status
```

**Output (services running)**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

Local Services:
  ✓ OK Backend
  ✓ OK Frontend
```

**Output (services stopped)**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

Local Services:
  -- Backend
  -- Frontend
```

**Advanced Status Checks**:
```powershell
# Check process details
Get-NetTCPConnection -LocalPort 8000,3000 | Select-Object LocalPort, State, OwningProcess

# Check Docker containers
docker ps
```

---

### `Test` - Verify Project Structure

**Purpose**: Validate required files exist

**Actions**:
Checks for presence of:
- `backend\app\main.py`
- `backend\requirements.txt`
- `frontend\package.json`
- `docker-compose.yml`

**Usage**:
```powershell
.\manage.ps1 Test
```

**Output (all files present)**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

Files:
  ✓ OK backend\app\main.py
  ✓ OK backend\requirements.txt
  ✓ OK frontend\package.json
  ✓ OK docker-compose.yml
```

**Output (missing files)**:
```
Files:
  !! backend\app\main.py
  ✓ OK backend\requirements.txt
  ...
```

---

### `Clean` - Remove Build Artifacts

**Purpose**: Clean up generated files and caches

**Actions**:
1. 🗑️ Delete all `__pycache__` directories (Python bytecode)
2. 🗑️ Remove `frontend\build` folder (production build)
3. 🗑️ Delete `*.log` files

**Usage**:
```powershell
.\manage.ps1 Clean
```

**Output**:
```
========================================
 AI Worker Productivity Dashboard
 Unified Workflow Manager
========================================

Cleaning...
OK
```

**When to Use**:
- Before committing to Git (clean working directory)
- After switching branches
- To free disk space
- When experiencing cache-related issues

**What Gets Deleted**:
```
backend/
  app/__pycache__/
  app/services/__pycache__/
  *.pyc
  *.log

frontend/
  build/
  *.log
```

**What Gets Preserved**:
- `node_modules/` (not deleted, use `npm ci` to reset)
- `.venv/` (not deleted, use `Setup` to recreate)
- Database files (`*.db`)
- Configuration files (`.env`)

---

### `Help` - Display Usage Guide

**Purpose**: Show comprehensive command reference

**Usage**:
```powershell
.\manage.ps1 Help
# OR
.\manage.ps1
```

**Output**: Full help text with examples and command descriptions

---

## Common Workflows

### First-Time Setup
```powershell
# 1. Clone repository
git clone https://github.com/bhartiinsan/ai-worker-productivity-dashboard
cd ai-worker-productivity-dashboard

# 2. Initialize environment
.\manage.ps1 Setup

# 3. Start services
.\manage.ps1 Start

# 4. Open browser to http://localhost:3000
```

### Daily Development
```powershell
# Morning: Start services
.\manage.ps1 Start

# Check if running
.\manage.ps1 Status

# Evening: Stop services
.\manage.ps1 Stop
```

### Docker Testing
```powershell
# Build and run containers
.\manage.ps1 StartDocker

# View logs
docker-compose logs -f

# Stop containers
.\manage.ps1 StopAll
```

### Troubleshooting
```powershell
# Services won't start (port conflict)
.\manage.ps1 Stop
.\manage.ps1 Start

# Clean build and restart
.\manage.ps1 Stop
.\manage.ps1 Clean
.\manage.ps1 Start

# Full reset
.\manage.ps1 StopAll
Remove-Item -Recurse backend\.venv, frontend\node_modules
.\manage.ps1 Setup
.\manage.ps1 Start
```

---

## Environment URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | React dashboard UI |
| **Backend** | http://localhost:8000 | FastAPI REST API |
| **API Docs (Swagger)** | http://localhost:8000/docs | Interactive API explorer |
| **API Docs (Redoc)** | http://localhost:8000/redoc | Alternative API docs |
| **Health Check** | http://localhost:8000/health | Backend health status |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (check output for details) |

---

## Advanced Usage

### Custom Port Numbers

**Backend**:
```powershell
# Edit manage.ps1 line ~49
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload  # Change 8000 to 8080
```

**Frontend**:
```powershell
# Set environment variable before npm start
$env:PORT = "3001"
npm start
```

### Run in Background (No Windows)

**Backend**:
```powershell
cd backend
& .\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
Start-Job -ScriptBlock { uvicorn app.main:app --host 0.0.0.0 --port 8000 }
```

**Frontend**:
```powershell
cd frontend
$env:BROWSER = "none"
Start-Job -ScriptBlock { npm start }
```

### Run Specific Services

**Backend Only**:
```powershell
cd backend
& .\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend Only** (requires backend running):
```powershell
cd frontend
npm start
```

---

## Troubleshooting

### "Python not found"
```powershell
# Install Python 3.11+
winget install Python.Python.3.11

# Verify installation
python --version
```

### "Docker not found"
```powershell
# Install Docker Desktop
winget install Docker.DockerDesktop

# Start Docker Desktop application
# Then retry: .\manage.ps1 StartDocker
```

### "Port already in use"
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Kill specific process
Stop-Process -Id <PID> -Force

# Or use workflow command
.\manage.ps1 Stop
```

### "Module not found" errors
```powershell
# Reinstall dependencies
.\manage.ps1 Clean
Remove-Item -Recurse backend\.venv
.\manage.ps1 Setup
```

---

## Related Documentation

- [README.md](../README.md) - Project overview
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System design
- [CONFIGURATION.md](./CONFIGURATION.md) - Environment variables
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Development guidelines

---

## Script Source

**Location**: `manage.ps1` (project root)

**Language**: PowerShell 5.1+

**Compatibility**: Windows 10/11 (WSL not required for local development)

**License**: MIT (same as project)
