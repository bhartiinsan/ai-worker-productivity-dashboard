# 🐳 Docker Installation Guide for Windows

## Quick Install (Recommended)

### Option 1: Docker Desktop (Easiest)

1. **Download Docker Desktop:**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - File size: ~500 MB

2. **Install Docker Desktop:**
   ```powershell
   # Run the installer
   # Follow the installation wizard
   # Restart your computer when prompted
   ```

3. **Verify Installation:**
   ```powershell
   docker --version
   # Expected: Docker version 24.0.x or higher
   
   docker compose version
   # Expected: Docker Compose version v2.x.x
   ```

4. **Start Docker Desktop:**
   - Open "Docker Desktop" from Start Menu
   - Wait for Docker engine to start (green indicator)
   - You should see "Docker Desktop is running"

### Option 2: Docker CLI Only (Lightweight)

If you don't need Docker Desktop UI:

```powershell
# Install using Chocolatey
choco install docker-desktop
```

---

## 🚀 Running Your Application with Docker

Once Docker is installed:

### Method 1: Docker Compose (One Command)

```powershell
cd C:\Users\BHARTI\OneDrive\Desktop\ai-worker-productivity-dashboard\ai-worker-productivity-dashboard

# Start all services
docker compose up --build

# Expected output:
# ✅ Building backend... Done
# ✅ Building frontend... Done
# ✅ Backend running on http://localhost:8000
# ✅ Frontend running on http://localhost:3000
# ✅ Database seeded with sample data
```

### Method 2: Using Startup Script

```powershell
# Windows
.\run_app.bat

# The script will:
# - Check if Docker is installed
# - Start Docker containers
# - Wait for services to be healthy
# - Auto-seed database
# - Open dashboard in browser
```

---

## 🔧 Troubleshooting

### Issue: "Docker daemon not running"

**Solution:**
1. Open Docker Desktop from Start Menu
2. Wait for green indicator (Docker engine starting)
3. Try command again

### Issue: "WSL 2 installation incomplete"

**Solution:**
```powershell
# Enable WSL 2 (required for Docker Desktop on Windows)
wsl --install
wsl --set-default-version 2

# Restart computer
```

### Issue: Port 8000 or 3000 already in use

**Solution:**
```powershell
# Stop existing processes
Get-Process | Where-Object {$_.ProcessName -eq "node" -or $_.ProcessName -eq "python"} | Stop-Process -Force

# Or change ports in docker-compose.yml:
# backend: "8001:8000"
# frontend: "3001:3000"
```

---

## 📋 Verify Docker Installation Checklist

Before running the application:

- [ ] Docker Desktop installed and running (green indicator)
- [ ] `docker --version` command works
- [ ] `docker compose version` command works
- [ ] WSL 2 enabled (for Windows users)
- [ ] Sufficient RAM (at least 4 GB allocated to Docker)
- [ ] Sufficient disk space (at least 2 GB free)

---

## ⏱️ Installation Time

| Step | Time Required |
|------|---------------|
| Download Docker Desktop | 5-10 minutes |
| Install Docker Desktop | 5 minutes |
| Restart computer | 2 minutes |
| Start Docker engine | 1 minute |
| **Total** | **13-18 minutes** |

---

## 🎯 After Installation

Once Docker is installed:

```powershell
# Navigate to project directory
cd C:\Users\BHARTI\OneDrive\Desktop\ai-worker-productivity-dashboard\ai-worker-productivity-dashboard

# Run the application
docker compose up --build

# Open browser
# http://localhost:3000 - Dashboard
# http://localhost:8000/docs - API Documentation

# Stop services (Ctrl+C in terminal, then:)
docker compose down
```

---

## 🔄 Alternative: Run Without Docker (Current Working Setup)

If you don't want to install Docker right now, your application is already running locally:

```powershell
# Backend (already running in separate window)
cd C:\Users\BHARTI\OneDrive\Desktop\ai-worker-productivity-dashboard\ai-worker-productivity-dashboard\backend
$env:PYTHONPATH="C:\Users\BHARTI\OneDrive\Desktop\ai-worker-productivity-dashboard\ai-worker-productivity-dashboard\backend"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend (separate window)
cd C:\Users\BHARTI\OneDrive\Desktop\ai-worker-productivity-dashboard\ai-worker-productivity-dashboard\frontend
npm start

# Seed database (separate window)
curl -X POST "http://localhost:8000/api/admin/seed?clear_existing=true"
```

**Dashboard:** http://localhost:3000  
**API Docs:** http://localhost:8000/docs

---

## 📞 Support

**Issue:** Docker installation fails  
**Solution:** Check system requirements (Windows 10/11 64-bit, virtualization enabled in BIOS)

**Issue:** Container build fails  
**Solution:** Check Docker has internet access for pulling base images

**Issue:** Services won't start  
**Solution:** Check logs with `docker compose logs backend` or `docker compose logs frontend`

---

**Last Updated:** January 22, 2026  
**Docker Version Required:** 24.0.0 or higher  
**Docker Compose Version Required:** 2.0.0 or higher
