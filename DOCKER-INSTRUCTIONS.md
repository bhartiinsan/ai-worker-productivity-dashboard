# Docker Deployment Instructions

## Prerequisites

### Install Docker Desktop

1. **Download Docker Desktop for Windows:**
   - Visit: https://www.docker.com/products/docker-desktop
   - Or use winget: `winget install Docker.DockerDesktop`

2. **Install Docker Desktop:**
   - Run the installer
   - Follow the installation wizard
   - Restart your computer when prompted

3. **Start Docker Desktop:**
   - Open Docker Desktop from Start Menu
   - Wait for Docker Engine to start (whale icon in system tray will be stable)

## Quick Start (Automated)

Simply run the automated script:

```batch
DOCKER-INSTALL-AND-START.bat
```

This script will:
- Check if Docker is installed
- Attempt to install Docker if missing
- Build both frontend and backend containers
- Start all services
- Show you the logs

## Manual Deployment

### Step 1: Verify Docker Installation

```bash
docker --version
docker-compose --version
```

### Step 2: Build and Start Containers

```bash
docker-compose up -d --build
```

### Step 3: Verify Containers Are Running

```bash
docker-compose ps
```

Expected output:
```
NAME                          STATUS    PORTS
factory-dashboard-backend     running   0.0.0.0:8000->8000/tcp
factory-dashboard-frontend    running   0.0.0.0:3000->80/tcp
```

### Step 4: Access the Application

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **API Redoc:** http://localhost:8000/redoc

## Data Seeding

The backend automatically seeds the database on first startup with:
- 6 workers (different shifts and departments)
- 6 workstations (different types and locations)
- 24 hours of sample AI events

To reseed data manually:
```bash
curl -X POST "http://localhost:8000/api/seed?clear_existing=true&hours_back=24"
```

Or access: http://localhost:8000/docs and use the `/api/seed` endpoint.

## Container Management

### View Logs

```bash
# All containers
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Stop Containers

```bash
docker-compose down
```

### Restart Containers

```bash
docker-compose restart
```

### Rebuild Containers (after code changes)

```bash
docker-compose down
docker-compose up -d --build
```

## Troubleshooting

### Port Already in Use

If port 3000 or 8000 is already in use:

1. Stop the conflicting process
2. Or modify `docker-compose.yml` ports:
   ```yaml
   ports:
     - "3001:80"  # Change 3000 to 3001
   ```

### Container Won't Start

Check logs:
```bash
docker-compose logs backend
docker-compose logs frontend
```

### Database Issues

Reset the database:
```bash
docker-compose down -v  # Remove volumes
docker-compose up -d --build
```

### Docker Not Running

Ensure Docker Desktop is running:
- Look for Docker whale icon in system tray
- It should be stable (not animating)
- If not, start Docker Desktop application

## Production Considerations

For production deployment:

1. **Use environment variables:**
   ```bash
   # Create .env file
   DATABASE_URL=postgresql://...
   CORS_ORIGINS=https://yourdomain.com
   ```

2. **Use external database:**
   - PostgreSQL recommended
   - Update `DATABASE_URL` in docker-compose.yml

3. **Enable HTTPS:**
   - Use a reverse proxy (nginx, Traefik)
   - Configure SSL certificates

4. **Resource limits:**
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '1'
             memory: 512M
   ```

## Architecture

```
┌─────────────────────────────────────────┐
│  Frontend Container (React + nginx)    │
│  Port: 3000 → 80                        │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  Backend Container (FastAPI + SQLite)  │
│  Port: 8000                             │
│  - Auto database initialization         │
│  - Auto data seeding on first run       │
│  - Health checks enabled                │
└─────────────────────────────────────────┘
```

## Next Steps

After successful deployment:

1. **Verify functionality:**
   - Open http://localhost:3000
   - Check if data is displayed
   - Test filters and metrics

2. **Explore API:**
   - Visit http://localhost:8000/docs
   - Try different endpoints
   - Review response schemas

3. **Monitor containers:**
   - `docker stats` - Resource usage
   - `docker-compose logs -f` - Live logs
   - Check health: http://localhost:8000/health
