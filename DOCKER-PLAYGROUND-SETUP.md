# 🐳 Running on Play with Docker (labs.play-with-docker.com)

## Quick Setup Guide

You're using an online Docker environment - follow these steps:

### Step 1: Clone Your Repository

In the Play with Docker terminal, run:

```bash
# Clone your project from GitHub
git clone https://github.com/bhartiinsan/ai-worker-productivity-dashboard.git

# Navigate to project directory
cd ai-worker-productivity-dashboard
```

### Step 2: Build and Run with Docker Compose

```bash
# Start all services (backend + frontend)
docker compose up --build
```

**Expected output:**
```
✅ Building backend... Done
✅ Building frontend... Done
✅ Backend running on port 8000
✅ Frontend running on port 3000
```

### Step 3: Access the Application

Once containers are running, you'll see ports 3000 and 8000 exposed.

**In Play with Docker:**
1. Look for "OPEN PORT" button at the top
2. Click it and enter **3000** (for frontend dashboard)
3. A new tab opens with your dashboard
4. Repeat for port **8000** (for API documentation)

**Alternative - Direct URLs:**
- Frontend: Click the `3000` badge that appears at the top
- Backend API: Click the `8000` badge that appears at the top

### Step 4: Seed Database

Open a new terminal in Play with Docker (click "+ ADD NEW INSTANCE" or use existing terminal):

```bash
# Seed sample data
docker exec -it ai-worker-productivity-dashboard-backend-1 curl -X POST http://localhost:8000/api/admin/seed?clear_existing=true
```

**OR use the frontend button:**
- Click "Reseed sample data" in the dashboard header

### Step 5: Test Worker Filter (Critical Requirement)

1. Open frontend dashboard (port 3000)
2. Look for worker filter dropdown in top-right header
3. Select "Worker 1" from dropdown
4. Verify leaderboard shows only Worker 1

---

## 🔧 Troubleshooting

### Issue: Ports not showing up

**Solution:**
```bash
# Check container status
docker compose ps

# View logs
docker compose logs backend
docker compose logs frontend
```

### Issue: Build fails

**Solution:**
```bash
# Clean up and retry
docker compose down
docker system prune -f
docker compose up --build
```

### Issue: Can't access dashboard

**Solution:**
```bash
# Check if frontend is running
docker compose logs frontend

# Verify port 3000 is exposed
docker ps
```

### Issue: Database not seeded

**Solution:**
```bash
# Seed manually
curl -X POST http://localhost:8000/api/admin/seed?clear_existing=true

# Check if backend is healthy
curl http://localhost:8000/health
```

---

## 📊 Verify Installation

Once running, check:

✅ **Frontend Dashboard** (port 3000):
- Factory KPIs visible
- Worker filter dropdown present
- Charts displaying data
- Event stream showing AI detections

✅ **Backend API** (port 8000):
- Visit `/docs` for Swagger documentation
- Visit `/health` for health check
- Visit `/api/factory/metrics` for metrics

✅ **Database:**
- 6 workers created
- 6 workstations created
- 2,365 events seeded

---

## 🎯 Quick Demo Script

For evaluators using Play with Docker:

```bash
# 1. Clone repository
git clone https://github.com/bhartiinsan/ai-worker-productivity-dashboard.git
cd ai-worker-productivity-dashboard

# 2. Start services
docker compose up --build

# 3. Wait for services to start (30-60 seconds)
# Look for: "Application startup complete"

# 4. Open ports 3000 and 8000 using OPEN PORT button

# 5. Test worker filter on dashboard

# 6. Check metrics accuracy:
curl http://localhost:8000/api/factory/metrics
```

Expected metrics after seeding:
- Active workers: 6
- Total production: ~1,256 units
- Average utilization: ~61.8%
- Production rate: ~14.07 units/hour

---

## ⏱️ Session Time Limit

**Play with Docker sessions last 4 hours**

If your session expires:
1. Start a new session at labs.play-with-docker.com
2. Repeat steps above (takes 2-3 minutes)

---

## 🚀 Alternative: Deploy to Cloud

For permanent deployment (no session timeout):

**Railway (Free Tier):**
```bash
# Your repo is already on GitHub
# 1. Visit railway.app
# 2. Connect GitHub repository
# 3. Auto-deploy in 10 minutes
```

**Render (Free Tier):**
```bash
# 1. Visit render.com
# 2. New Web Service → Connect GitHub
# 3. Auto-deploy in 12 minutes
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides.

---

## 📞 Support

**Issue:** Containers won't start  
**Solution:** Check Docker Compose logs: `docker compose logs`

**Issue:** Ports not accessible  
**Solution:** Wait 60 seconds for services to fully start, then refresh

**Issue:** Empty dashboard  
**Solution:** Seed database: `curl -X POST http://localhost:8000/api/admin/seed?clear_existing=true`

---

**Last Updated:** January 22, 2026  
**Play with Docker:** https://labs.play-with-docker.com  
**Repository:** https://github.com/bhartiinsan/ai-worker-productivity-dashboard
