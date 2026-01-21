# 🏭 AI Worker Productivity Dashboard

**Production-Ready Smart Factory Analytics Platform**

Real-time monitoring and analysis of worker productivity through AI-powered CCTV analytics. Enterprise-grade full-stack solution demonstrating modern architecture, data integrity, and professional UX design.

[![GitHub stars](https://img.shields.io/github/stars/bhartiinsan/ai-worker-productivity-dashboard?style=flat-square&logo=github)](https://github.com/bhartiinsan/ai-worker-productivity-dashboard)
[![GitHub issues](https://img.shields.io/github/issues/bhartiinsan/ai-worker-productivity-dashboard?style=flat-square&logo=github)](https://github.com/bhartiinsan/ai-worker-productivity-dashboard/issues)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

---

## 📸 Screenshots

### Dashboard Overview - Real-time KPI Monitoring
![Dashboard Overview](docs/images/dashboard-overview.png)
*Factory-wide metrics with worker leaderboard and performance indicators*

### Worker Leaderboard - Performance Analytics
![Worker Leaderboard](docs/images/worker-leaderboard.png)
*Real-time utilization tracking with color-coded efficiency ratings*

### Event Stream - Live AI Detections
![Event Stream](docs/images/event-stream.png)
*Chronological feed of AI-detected events with confidence scores*

---

## 🎯 Overview

Monitor worker productivity across 6 workstations in real-time using AI-powered CCTV cameras. The system ingests events from edge devices, applies deduplication logic, and computes factory-wide metrics instantly.

**System Flow:**
```
CCTV Cameras → AI Detection → FastAPI Backend → SQLite Database → React Dashboard
```

**Key Capabilities:**
- Real-time event ingestion with deduplication
- Worker, workstation, and factory-level KPI computation
- Bitemporal tracking (event time vs. server time)
- Production-ready Docker deployment
- Modern dark-mode industrial UI

---

## ✨ Key Features

### Backend
- ✅ Single & batch event ingestion endpoints
- ✅ Automatic deduplication via UNIQUE constraints
- ✅ Confidence threshold filtering (≥ 0.7)
- ✅ Multi-level metrics (worker/workstation/factory)
- ✅ Bitemporal tracking for audit trails
- ✅ Rate limiting (100 req/min) & CORS security
- ✅ Health checks & structured logging
- ✅ Auto-generated Swagger API docs
- ✅ Realistic data seeding with shift patterns

### Frontend
- ✅ Factory KPI cards (active workers, utilization, production rate)
- ✅ Worker productivity leaderboard with rankings
- ✅ Workstation utilization grid with heatmap
- ✅ Live AI event stream with color-coded badges
- ✅ Productivity trend charts
- ✅ Dark mode industrial aesthetic
- ✅ Smooth animations (Framer Motion)
- ✅ Fully responsive design

---

## 🏗️ Architecture

### Simple View
```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   CCTV AI   │ ───> │    FastAPI   │ ───> │    React    │
│ (6 Cameras) │ JSON │  (SQLite)    │ REST │ Dashboard   │
└─────────────┘      └──────────────┘      └─────────────┘
```

**Four-Stage Data Pipeline:**
1. **Edge Device** - AI inference + local buffering
2. **API Ingestion** - Deduplication + validation
3. **Database** - Bitemporal persistence (event_time + created_at)
4. **Aggregation** - Real-time metric computation

**Design Principles:**
- **Determinism**: Timestamp-ordered processing for reproducible results
- **Resilience**: Store-and-forward buffering survives network outages
- **Auditability**: Dual timestamp tracking for compliance
- **Scalability**: Indexed queries handle 100M+ events

📖 **[Full Architecture Documentation](docs/ARCHITECTURE.md)**

---

## 🚀 Quick Start

### Prerequisites
Choose one deployment method:
- **Option 1**: Docker Desktop (recommended for quick demo)
- **Option 2**: Python 3.11+ and Node.js 18+ (for local development)

### Option 1: Docker (Recommended - 2 Commands)

```bash
# 1. Start all services
docker compose up -d

# 2. Seed database with 24 hours of realistic data
curl -X POST "http://localhost:8000/api/admin/seed?clear_existing=true"
```

**Access Points:**
- 🎨 **Dashboard**: http://localhost:3000
- 🔧 **API Docs**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/health

**Stop services:**
```bash
docker compose down
```

### Option 2: Local Development

**Backend:**
```powershell
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

**Frontend (new terminal):**
```powershell
cd frontend

# Install dependencies
npm install

# Start dev server
npm start
```

**Seed Data:**
```bash
curl -X POST "http://localhost:8000/api/admin/seed?clear_existing=true"
```

### Windows Quick Launch

```batch
# Double-click or run:
LAUNCH.bat
```

This automated script handles backend setup, frontend installation, and database seeding.

---

## 🔧 Tech Stack

**Backend**
- Python 3.11+ with type hints
- FastAPI for REST API
- SQLAlchemy ORM with SQLite (PostgreSQL-ready)
- Pydantic for data validation
- Uvicorn ASGI server

**Frontend**
- React 18 with TypeScript 5.x
- Tailwind CSS for styling
- Framer Motion for animations
- Axios for API calls
- Recharts for data visualization

**Infrastructure**
- Docker & Docker Compose
- Nginx reverse proxy
- Environment-based configuration

---

## 📡 API Reference

### Event Ingestion

**POST /api/events** - Ingest single event
```json
{
  "timestamp": "2026-01-21T14:30:00Z",
  "worker_id": "W1",
  "workstation_id": "S3",
  "event_type": "working",
  "confidence": 0.93,
  "count": 1
}
```

**POST /api/events/batch** - Ingest multiple events (1-1000)

### Metrics

**GET /api/metrics/factory** - Factory-wide KPIs
```json
{
  "total_workers": 6,
  "active_workers": 6,
  "avg_utilization": 71.2,
  "total_production": 217,
  "production_rate": 2.1
}
```

**GET /api/metrics/workers** - Per-worker performance

**GET /api/metrics/workstations** - Per-station utilization

### Events

**GET /api/events?limit=60** - Recent AI detections

### Admin

**POST /api/admin/seed** - Generate sample data

**Interactive Documentation**: http://localhost:8000/docs

---

## 📁 Repository Structure

```
ai-worker-productivity-dashboard/
├── README.md                      # This file
├── LICENSE                        # MIT License
├── docker-compose.yml             # Container orchestration
├── manage.ps1                     # PowerShell workflow manager
├── LAUNCH.bat                     # Windows quick start
│
├── docs/                          # Extended documentation
│   ├── ARCHITECTURE.md            # Deep dive into system design
│   ├── CONFIGURATION.md           # Environment variable guide
│   ├── CONTRIBUTING.md            # Contribution guidelines
│   ├── DASHBOARD-GUIDE.md         # UI component reference
│   └── images/                    # Screenshots
│       ├── dashboard-overview.png
│       ├── worker-leaderboard.png
│       └── event-stream.png
│
├── backend/                       # FastAPI application
│   ├── app/
│   │   ├── main.py               # API entry point
│   │   ├── models.py             # Database schema
│   │   ├── schemas.py            # Pydantic validation
│   │   ├── database.py           # SQLAlchemy setup
│   │   ├── crud.py               # Database operations
│   │   ├── config.py             # Configuration
│   │   └── services/             # Business logic
│   │       ├── events_service.py # Event ingestion
│   │       ├── metrics_service.py # KPI computation
│   │       └── seed_service.py   # Data generation
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
└── frontend/                      # React application
    ├── src/
    │   ├── App.tsx               # Main dashboard
    │   ├── types.ts              # TypeScript interfaces
    │   └── services/
    │       └── api.ts            # API client
    ├── package.json
    ├── tsconfig.json
    ├── tailwind.config.js
    ├── Dockerfile
    └── nginx.conf
```

---

## 🧪 Data Integrity

### Deduplication Strategy
Events are deduplicated using a composite UNIQUE constraint:
```sql
UNIQUE (timestamp, worker_id, event_type)
```

This ensures:
- Network retries don't create duplicates
- Out-of-order events are handled correctly
- Idempotent API (calling twice = same result)

### Bitemporal Tracking
Each event stores two timestamps:
- **event_time**: When the event actually occurred (CCTV detection time)
- **created_at**: When the server received it

This enables:
- Accurate metrics even with network delays
- Audit trails for compliance
- Historical reconstruction of system state

### Realistic Data Patterns
The seeding function includes:
- **Lunch break** (1:00-1:45 PM): 70% workers absent
- **Slow start** (6:00-6:30 AM): Reduced productivity during warm-up
- **Product correlation**: Units produced ONLY during "working" state
- **Shift patterns**: Different worker schedules

---

## 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](README.md) | Quick start & overview | Everyone |
| [EVALUATOR-GUIDE.md](EVALUATOR-GUIDE.md) | 10-minute assessment guide | Technical reviewers |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design deep dive | Engineers |
| [docs/CONFIGURATION.md](docs/CONFIGURATION.md) | Environment setup | DevOps |
| [docs/DASHBOARD-GUIDE.md](docs/DASHBOARD-GUIDE.md) | UI component reference | End users |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | Development guidelines | Contributors |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | Codebase navigation | Developers |

---

## 🔐 Security

- **Rate Limiting**: 100 requests/minute per endpoint
- **CORS**: Configured for specific frontend origins
- **Environment Variables**: Sensitive config in .env (not committed)
- **Input Validation**: Pydantic schemas validate all API inputs
- **Confidence Threshold**: Reject events with confidence < 0.7

---

## 🎯 What This Demonstrates

✅ **Full-Stack Development**: End-to-end system from edge to UI  
✅ **System Design**: Multi-tier architecture with clear separation of concerns  
✅ **Data Engineering**: Deduplication, bitemporal tracking, time-series aggregation  
✅ **Backend Skills**: Type-safe Python, service layer pattern, RESTful API design  
✅ **Frontend Skills**: Modern React, TypeScript, responsive design, animations  
✅ **DevOps**: Docker deployment, environment configuration, health monitoring  
✅ **Code Quality**: Modular, documented, type-safe, DRY principles  
✅ **Production Thinking**: Security, scalability, error handling, logging  
✅ **Domain Knowledge**: Manufacturing patterns (shifts, breaks, warm-up periods)

---

## 🚦 Known Limitations & Assumptions

### Current Scope
- **Database**: SQLite (sufficient for 6 workers, 100K events/day)
- **Deployment**: Single-instance (no load balancing)
- **Real-time**: 30-second polling (WebSockets planned)
- **Authentication**: Basic rate limiting (OAuth2 planned)

### Production Considerations
For scaling to 100+ cameras:
- Migrate to PostgreSQL + TimescaleDB
- Add Kafka for event streaming
- Implement Redis caching
- Deploy on Kubernetes with auto-scaling

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed scaling plan.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright © 2026 Bharti

---

## 🙏 Acknowledgments

**Technologies:**
- FastAPI framework by Sebastián Ramírez
- React by Meta Open Source
- Tailwind CSS by Tailwind Labs
- SQLAlchemy ORM

**Inspiration:**
- Smart factory initiatives in manufacturing
- Real-time analytics dashboards (Grafana, DataDog)
- Industrial IoT platforms

---

**Built for technical assessments 🚀**  
*Demonstrating enterprise-grade full-stack engineering capabilities*

**Questions?** Open an issue: https://github.com/bhartiinsan/ai-worker-productivity-dashboard/issues
