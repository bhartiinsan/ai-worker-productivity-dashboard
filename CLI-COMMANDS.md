# CLI Commands Reference & System Workflow

## 🏗️ System Architecture & Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     AI WORKER PRODUCTIVITY DASHBOARD             │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Frontend   │  HTTP   │   Backend    │  ORM    │   Database   │
│  React + TS  │ ◄─────► │   FastAPI    │ ◄─────► │   SQLite     │
│  Port 3000   │  REST   │  Port 8000   │SQLAlchemy│productivity.db│
└──────────────┘         └──────────────┘         └──────────────┘
      │                         │                         │
      │                         │                         │
      ▼                         ▼                         ▼
  - Chart.js            - Rate Limiting           - Workers (6)
  - Framer Motion       - CORS Security           - Workstations (6)
  - Auto-refresh        - Health Checks           - AI Events (1164)
  - Confidence Filter   - Model Monitoring        - Deduplication
```

### Data Flow Workflow

```
1. USER INTERACTION
   │
   ├─► Visit http://localhost:3000
   │
   └─► Dashboard loads → Fetches data via API calls

2. API REQUEST FLOW
   │
   ├─► GET /api/metrics/factory
   ├─► GET /api/metrics/workers
   ├─► GET /api/metrics/workstations
   └─► GET /api/events?limit=60
       │
       └─► Backend processes request
           │
           ├─► Rate limiting check (200/min)
           ├─► CORS validation
           ├─► Database query (SQLAlchemy ORM)
           └─► Return JSON response

3. DATABASE OPERATIONS
   │
   ├─► Read: metrics_service.py calculates aggregations
   ├─► Write: Events stored with UNIQUE constraints
   └─► Deduplication: (worker_id, workstation_id, event_type, event_time)

4. REAL-TIME UPDATES
   │
   ├─► Auto-refresh: Every 30 seconds
   ├─► User can manually reseed data
   └─► Confidence filter: Client-side filtering (<80%)
```

---

## 🚀 Quick Start Commands

### One-Command Launch (Recommended)

```powershell
# Launch everything (backend + frontend)
.\LAUNCH.bat
```

### Docker Deployment

```powershell
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

---

## 📦 Environment Setup Commands

### 1. Backend Setup

```powershell
# Navigate to project root
cd C:\Users\BHARTI\OneDrive\Desktop\Dashboard

# Create virtual environment
python -m venv backend\.venv

# Activate virtual environment
& backend\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend\requirements.txt

# Or use direct path
& backend\.venv\Scripts\pip.exe install -r backend\requirements.txt

# Verify installation
& backend\.venv\Scripts\pip.exe list
```

### 2. Frontend Setup

```powershell
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Verify installation
npm list --depth=0

# Return to project root
cd ..
```

---

## 🎯 Running Services

### Start Backend Only

```powershell
# Method 1: Using batch file
.\BACKEND.bat

# Method 2: Manual command
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Method 3: Production mode (no reload)
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Start Frontend Only

```powershell
# Method 1: Using batch file
.\FRONTEND.bat

# Method 2: Manual command
cd frontend
npm start

# Frontend will open browser automatically at http://localhost:3000
```

### Start Both Services

```powershell
# Automated launcher
.\LAUNCH.bat

# Manual (open 2 terminals)
# Terminal 1:
.\BACKEND.bat

# Terminal 2:
.\FRONTEND.bat
```

---

## 🗄️ Database Operations

### Initialize Database

```powershell
# Database is created automatically on first run
# Location: backend/productivity.db
```

### Seed Sample Data

```powershell
# Using API endpoint (backend must be running)
curl -X POST "http://localhost:8000/api/admin/seed?clear_existing=true"

# Or use Invoke-RestMethod (PowerShell)
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/admin/seed?clear_existing=true"

# Parameters:
# - clear_existing=true : Delete existing data first
# - hours=24 : Generate data for 24 hours (default)
```

### Reset Database

```powershell
# Stop backend first
Stop-Process -Name python -Force

# Delete database file
Remove-Item backend\productivity.db -Force

# Restart backend - database will be recreated
.\BACKEND.bat

# Reseed data
curl -X POST "http://localhost:8000/api/admin/seed?clear_existing=true"
```

---

## 🔍 Testing & Verification Commands

### Check Backend Health

```powershell
# Health check endpoint
curl http://localhost:8000/health

# PowerShell method
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Expected response:
# {
#   "status": "healthy",
#   "timestamp": "2026-01-21T...",
#   "database": "healthy",
#   "environment": "development"
# }
```

### Check Port Usage

```powershell
# Check if backend is running (port 8000)
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# Check if frontend is running (port 3000)
Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue

# View all ports in use
Get-NetTCPConnection | Where-Object {$_.State -eq "Listen"} | Select-Object LocalPort, OwningProcess | Sort-Object LocalPort
```

### Test API Endpoints

```powershell
# Factory metrics
curl http://localhost:8000/api/metrics/factory

# Worker metrics
curl http://localhost:8000/api/metrics/workers

# Workstation metrics
curl http://localhost:8000/api/metrics/workstations

# Recent events (last 60)
curl http://localhost:8000/api/events?limit=60

# Model health (NEW)
curl http://localhost:8000/api/metrics/model-health

# Efficiency heatmap (NEW)
curl http://localhost:8000/api/metrics/efficiency-heatmap

# Interactive API docs
start http://localhost:8000/docs
```

---

## 🛠️ Process Management

### View Running Processes

```powershell
# Find Python processes
Get-Process python -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, CPU

# Find Node processes
Get-Process node -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, CPU

# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object OwningProcess
```

### Stop Services

```powershell
# Stop backend
Stop-Process -Name python -Force -ErrorAction SilentlyContinue

# Stop frontend
Stop-Process -Name node -Force -ErrorAction SilentlyContinue

# Stop both
Stop-Process -Name "python","node" -Force -ErrorAction SilentlyContinue

# Stop specific port (8000)
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | 
    Select-Object -ExpandProperty OwningProcess -Unique | 
    ForEach-Object { Stop-Process -Id $_ -Force }
```

---

## 🐛 Troubleshooting Commands

### Fix Corrupted Virtual Environment

```powershell
# Remove old venv
Remove-Item -Path "backend\.venv" -Recurse -Force

# Create new venv
python -m venv backend\.venv

# Install dependencies
& backend\.venv\Scripts\pip.exe install -r backend\requirements.txt
```

### Fix Frontend Dependencies

```powershell
# Remove node_modules
cd frontend
Remove-Item -Path "node_modules" -Recurse -Force
Remove-Item -Path "package-lock.json" -Force

# Reinstall
npm install

# Clear cache if issues persist
npm cache clean --force
npm install
```

### Check for Errors

```powershell
# Test backend startup
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test frontend compilation
cd frontend
npm run build

# Check TypeScript errors
npm run build
```

### Verify Python Environment

```powershell
# Check Python version
python --version

# Check pip version
& backend\.venv\Scripts\pip.exe --version

# List installed packages
& backend\.venv\Scripts\pip.exe list

# Check for missing packages
& backend\.venv\Scripts\pip.exe check
```

---

## 🐳 Docker Commands

### Build and Run

```powershell
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Container Management

```powershell
# List running containers
docker-compose ps

# Stop containers
docker-compose down

# Restart services
docker-compose restart

# Remove volumes (full reset)
docker-compose down -v
```

### Debugging Docker

```powershell
# Enter backend container shell
docker exec -it factory-dashboard-backend /bin/bash

# Enter frontend container shell
docker exec -it factory-dashboard-frontend /bin/sh

# View container logs
docker logs factory-dashboard-backend
docker logs factory-dashboard-frontend

# Inspect container
docker inspect factory-dashboard-backend
```

---

## 📊 Development Workflow

### Daily Development Cycle

```powershell
# 1. Start development environment
.\LAUNCH.bat

# 2. Make code changes in VS Code

# 3. Backend auto-reloads (--reload flag)
#    Frontend auto-reloads (webpack dev server)

# 4. Test changes at http://localhost:3000

# 5. Stop services when done
Stop-Process -Name "python","node" -Force
```

### Before Committing Code

```powershell
# 1. Test backend
cd backend
.\.venv\Scripts\python.exe -m pytest  # If tests exist

# 2. Build frontend
cd frontend
npm run build

# 3. Check for TypeScript errors
npm run build

# 4. Test Docker deployment
docker-compose up -d
# Verify at http://localhost:3000
docker-compose down
```

---

## 🔐 Production Deployment

### Prepare for Production

```powershell
# 1. Update environment variables
# Edit .env.example and create .env

# 2. Build Docker images
docker-compose build --no-cache

# 3. Run in production mode
docker-compose up -d

# 4. Monitor logs
docker-compose logs -f

# 5. Health checks
curl http://localhost:8000/health
```

### Performance Testing

```powershell
# Test rate limiting (200 requests/min)
for ($i=1; $i -le 10; $i++) {
    Invoke-RestMethod -Uri "http://localhost:8000/api/metrics/factory"
    Write-Host "Request $i completed"
}

# Test model health endpoint
Invoke-RestMethod -Uri "http://localhost:8000/api/metrics/model-health"

# Test efficiency heatmap
Invoke-RestMethod -Uri "http://localhost:8000/api/metrics/efficiency-heatmap"
```

---

## 📝 Useful Maintenance Commands

### Cleanup Commands

```powershell
# Remove Python cache
Get-ChildItem -Path backend -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force

# Remove TypeScript build
Remove-Item -Path "frontend\build" -Recurse -Force

# Clean Docker
docker system prune -a

# Full cleanup (WARNING: removes everything)
Remove-Item backend\.venv -Recurse -Force
Remove-Item frontend\node_modules -Recurse -Force
Remove-Item frontend\build -Recurse -Force
Remove-Item backend\productivity.db -Force
```

### Update Dependencies

```powershell
# Update Python packages
& backend\.venv\Scripts\pip.exe install --upgrade -r backend\requirements.txt

# Update Node packages
cd frontend
npm update

# Check for outdated packages
npm outdated
```

---

## 🎯 Quick Reference: Common Tasks

| Task | Command |
|------|---------|
| Start everything | `.\LAUNCH.bat` |
| Start backend only | `.\BACKEND.bat` |
| Start frontend only | `.\FRONTEND.bat` |
| Docker deployment | `docker-compose up -d` |
| Check health | `curl http://localhost:8000/health` |
| Reseed data | `curl -X POST http://localhost:8000/api/admin/seed?clear_existing=true` |
| View API docs | `start http://localhost:8000/docs` |
| Stop all | `Stop-Process -Name "python","node" -Force` |
| Check ports | `Get-NetTCPConnection -LocalPort 8000,3000` |
| Reset database | `Remove-Item backend\productivity.db -Force` |

---

## 🔗 Important URLs

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Model Health**: http://localhost:8000/api/metrics/model-health
- **Efficiency Heatmap**: http://localhost:8000/api/metrics/efficiency-heatmap

---

## 📚 Files Created & Purpose

```
Dashboard/
├── LAUNCH.bat              # One-command launcher (backend + frontend)
├── BACKEND.bat             # Start backend only
├── FRONTEND.bat            # Start frontend only
├── DOCKER-START.bat        # Docker deployment launcher
├── docker-compose.yml      # Docker orchestration config
├── README.md               # Complete project documentation
├── FINAL-SUMMARY.md        # Features & submission guide
├── CLI-COMMANDS.md         # This file - all CLI commands
│
├── backend/
│   ├── .venv/              # Python virtual environment
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend Docker image
│   ├── productivity.db     # SQLite database (auto-created)
│   └── app/
│       ├── main.py         # FastAPI application
│       ├── models.py       # Database models
│       ├── schemas.py      # Pydantic validation schemas
│       ├── crud.py         # Database operations
│       ├── database.py     # Database connection
│       ├── config.py       # Environment configuration
│       ├── middleware.py   # Rate limiting middleware
│       └── services/
│           ├── metrics_service.py   # Metrics calculations
│           ├── events_service.py    # Event processing
│           └── seed_service.py      # Data seeding
│
└── frontend/
    ├── node_modules/       # Node dependencies (npm install)
    ├── package.json        # Node dependencies list
    ├── Dockerfile          # Frontend Docker image
    ├── nginx.conf          # Nginx web server config
    ├── build/              # Production build (npm run build)
    └── src/
        ├── App.tsx         # Main React component
        ├── types.ts        # TypeScript type definitions
        └── services/
            └── api.ts      # API client functions
```

---

## ✅ System Requirements

- **Python**: 3.11+ (check: `python --version`)
- **Node.js**: 20+ (check: `node --version`)
- **npm**: 10+ (check: `npm --version`)
- **Docker**: Optional (check: `docker --version`)
- **OS**: Windows with PowerShell 5.1+

---

**Last Updated**: January 21, 2026  
**Version**: Production-Ready 1.0  
**Status**: ✅ All features working
