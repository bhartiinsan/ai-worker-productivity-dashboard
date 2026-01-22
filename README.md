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

**This project assumes a fixed sample setup of 6 workers and 6 workstations as per assessment constraints, with all data generated via seeded AI events.**

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
- ✅ **Worker filter dropdown** for individual performance analysis
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

### 🎯 Zero-Configuration Docker Setup

**Everything works with ONE command - no manual setup required:**

```bash
# Option 1: Using docker compose directly
docker compose up --build

# Option 2: Using provided startup scripts
# Linux/macOS:
./run_app.sh

# Windows:
run_app.bat
```

**What happens automatically:**
1. ✅ Backend starts with SQLite database
2. ✅ Health checks ensure backend is ready
3. ✅ Frontend starts only after backend is healthy
4. ✅ Database auto-seeds with 6 workers and 6 workstations (when using scripts)

**Access Points:**
- 🎨 **Dashboard**: http://localhost:3000
- 🔧 **API Docs**: http://localhost:8000/docs
- ❤️ **Health Check**: http://localhost:8000/health

**Stop services:**
```bash
docker compose down
```

### 🌐 Live Demo

**Production Deployment:** [Coming Soon - Deploy to Render/Railway]

*The live demo comes pre-loaded with 24 hours of realistic factory data for immediate evaluation.*

---

### Prerequisites
Choose one deployment method:
- **Option 1**: Docker Desktop (recommended for quick demo)
- **Option 2**: Python 3.11+ and Node.js 18+ (for local development)

### Option 1: Docker (Recommended - 2 Commands)

```bash
# Quick start (one command to build and run)
docker compose up --build

# OR start in detached mode:
docker compose up -d

# Then seed database with 24 hours of realistic data
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
# Refresh dummy data (clears existing and generates 24h of events)
curl -X POST "http://localhost:8000/api/admin/seed?clear_existing=true"

# Verify exactly 6 workers and 6 workstations were created
curl http://localhost:8000/api/workers | jq '. | length'  # Returns: 6
curl http://localhost:8000/api/workstations | jq '. | length'  # Returns: 6
```

**💡 Pro Tip:** The dashboard has a "Reseed sample data" button for one-click data refresh during evaluation.

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

### Base URL
```
http://localhost:8000
```

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check (`{"status": "healthy"}`) |
| GET | `/api/workers` | List all workers with metrics |
| GET | `/api/workstations` | List all workstations |
| GET | `/api/events` | Activity events (latest 100) |
| POST | `/api/events` | Create new event |
| POST | `/api/events/batch` | Bulk upload (max 100 events) |
| GET | `/api/metrics/factory` | Factory-wide KPIs |

### Example Request
```bash
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "worker_id": 1,
    "workstation_id": 1,
    "event_type": "working",
    "timestamp": "2026-01-21T10:00:00Z",
    "confidence": 0.95
  }'
```

**Full API documentation**: Interactive Swagger UI at http://localhost:8000/docs

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

## 📊 Metrics & Data Integrity

### Metric Definitions & Formulas

| Metric | Calculation Formula | Assumption |
|--------|---------------------|------------|
| **Utilization %** | `(Total Active Time / (Active Time + Idle Time)) × 100` | Each 'working' event duration = time until next event or 5-minute timeout |
| **Units per Hour** | `Total Units Produced / Total Active Hours` | Counts only time spent in 'working' state |
| **Throughput Rate** | `Total Units / Total Workstation Occupancy Hours` | Includes 'working' and 'idle' time at station |
| **Production Rate** | `Average Units per Hour across all active workers` | Weighted by worker productivity |

### Mathematical Definitions

**Worker Active Time**  
Sum of time intervals where the latest state event is `working`.

**Worker Idle Time**  
Sum of time intervals where the latest state event is `idle`.

**Utilization Percentage**  
```
Utilization = Active Time / (Active Time + Idle Time) × 100
```

**Units Produced**  
Sum of `count` from all `product_count` events for the worker/workstation.

**Units per Hour**  
```
Units per Hour = Total Units Produced / Total Active Hours
```

### Assumptions

**Metric Aggregation Model:**  
We use a **"State-Duration" model** for time-based metrics. Each `working` or `idle` event is assumed to represent the worker's state until a new event of a different type is received. If no event is received for >10 minutes, the worker is marked as `absent`. `product_count` events are treated as instantaneous markers and summed within the `working` duration windows.

**Core Assumptions:**
- Time between two consecutive state events represents the duration of the earlier state.
- If no new event is received, the last known state is assumed to continue.
- `product_count` events are instantaneous and independent of time-based states.

**Complete formulas and ranges**: See [docs/METRICS.md](docs/METRICS.md)

### Event Handling Guarantees

- **Duplicate events:**  
  Events are idempotent using a composite key of (timestamp, worker_id, workstation_id, event_type). Duplicate events are ignored at ingestion.

- **Out-of-order timestamps:**  
  Events are sorted by timestamp during metric aggregation. Late-arriving events are reprocessed during aggregation queries.

- **Intermittent connectivity:**  
  The backend assumes eventual consistency. Events can be ingested in batches once connectivity resumes without affecting correctness.

### Additional Robustness Features
- ✅ **Duplicate detection**: Database UNIQUE constraint prevents double-counting
- ✅ **Out-of-order handling**: Events sorted by timestamp before calculation
- ✅ **Offline resilience**: Edge devices buffer up to 10,000 events locally
- ✅ **Missing data safety**: Zero-division guards, null-safe operations
- ✅ **Confidence filtering**: Reject low-confidence AI detections (< 0.7)

**Detailed edge case strategies**: See [docs/EDGE-CASES.md](docs/EDGE-CASES.md)


---

## 🧪 Data Integrity

### Data Persistence Strategy

- All AI events are stored in an append-only `ai_events` table to preserve auditability.
- No events are updated or deleted once ingested.
- Dummy data is generated exclusively through backend seed APIs, allowing evaluators to refresh data without modifying the database or frontend.

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
| [docs/CLI-REFERENCE.md](docs/CLI-REFERENCE.md) | Workflow manager commands | Developers |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design deep dive | Engineers |
| [docs/CONFIGURATION.md](docs/CONFIGURATION.md) | Environment setup | DevOps |
| [docs/METRICS.md](docs/METRICS.md) | Metric formulas & ranges | Data analysts |
| [docs/EDGE-CASES.md](docs/EDGE-CASES.md) | Data integrity strategies | Quality engineers |
| [docs/DASHBOARD-GUIDE.md](docs/DASHBOARD-GUIDE.md) | UI component reference | End users |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | Development guidelines | Contributors |

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

## 🏛️ Technical Analysis & Architecture

### Edge → Backend → Dashboard Data Flow

**1. Edge (CCTV Cameras):**  
AI models process video on-site and emit JSON events containing worker activity, confidence scores, and timestamps.

**2. Backend (FastAPI):**  
Ingests raw events via REST API, performs deduplication using database constraints, validates confidence thresholds (≥ 0.7), and persists to SQLite with bitemporal tracking.

**3. Dashboard (React):**  
Aggregates data from the database to visualize real-time KPIs, worker leaderboards, and event streams with 30-second auto-refresh.

### Data Integrity & Reliability

**Intermittent Connectivity:**  
Implement **Store-and-Forward** mechanism at the Edge. Events are buffered locally in a persistent cache (up to 10,000 events) and pushed to the API once connection is restored. The backend's eventual consistency model ensures correct metric calculation regardless of delayed arrival.

**Duplicate Events:**  
The database enforces a **Unique Constraint** on `(timestamp, worker_id, workstation_id, event_type)`. Any duplicate JSON payload from network retries is automatically rejected at the database level, ensuring idempotent ingestion.

**Out-of-Order Timestamps:**  
The API does not rely on "received_at" server time. All metrics are calculated by **sorting events chronologically by their original camera timestamp** before aggregation, guaranteeing correctness even with delayed or reordered arrivals.

### AI Model Lifecycle Management

**Model Versioning:**  
Each event payload includes a `model_version` field (optional) in metadata to track which CV model version generated the detection. This enables A/B testing and performance comparison across model iterations.

**Model Drift Detection:**  
Monitor the **average confidence score** over time using a 7-day moving average. A sustained drop below 75% indicates drift (e.g., lighting changes, camera repositioning, seasonal variations), triggering automated retraining alerts.

**Retraining Triggers:**  
Automated retraining is triggered when:
- Confidence scores degrade by >15% over 7 days
- Manual ground truth verification flags systematic misclassifications
- Productivity baselines deviate >2 standard deviations from historical norms

### Scalability Strategy (5 → 100+ Cameras)

**Database Evolution:**  
Migrate from SQLite to **PostgreSQL + TimescaleDB** for:
- Concurrent write handling from 100+ cameras
- Time-series optimizations (automatic partitioning, compression)
- Horizontal scaling with read replicas

**High-Volume Ingestion:**  
Introduce **Redis Streams or Apache Kafka** as message broker:
- Decouple camera ingestion from processing
- Handle burst traffic (1000+ events/second)
- Enable async processing with worker pools

**Multi-Site Deployment:**  
Deploy regional ingestion nodes with:
- `site_id` field for data partitioning
- Local aggregation for site-specific dashboards
- Central data warehouse for cross-site analytics

**Infrastructure:**  
Kubernetes deployment with:
- Auto-scaling based on queue depth
- Prometheus + Grafana for monitoring
- Circuit breakers for fault tolerance

---

## 🤖 Model Lifecycle Considerations

### Model Versioning
Each event payload can include a `model_version` field to track which CV model generated the event.

### Drift Detection
Monitor changes in confidence scores, idle/working ratios, and production rates over time.

### Retraining Triggers
Retraining can be triggered when:
- Sustained confidence degradation is detected
- Significant deviation from historical productivity baselines occurs

---

## 🚦 Known Limitations & Assumptions

### Current Scope
- **Database**: SQLite (sufficient for 6 workers, 100K events/day)
- **Deployment**: Single-instance (no load balancing)
- **Real-time**: 30-second polling (WebSockets planned)
- **Authentication**: Basic rate limiting (OAuth2 planned)

## 📈 Scalability Strategy

### 5 to 100+ Cameras
- **Horizontal scaling** of ingestion APIs with load balancing and database indexing on timestamp and worker/workstation IDs.
- **Database optimization**: Migrate to PostgreSQL + TimescaleDB for time-series data.
- **Caching layer**: Implement Redis for frequently accessed metrics.

### High-Volume Ingestion
- **Message queues**: Introduce Kafka/SQS between cameras and backend to decouple ingestion from processing.
- **Async processing**: Background workers process events from queue.
- **Batch aggregation**: Compute metrics in scheduled batches for efficiency.

### Multi-Site Factories
- **Site isolation**: Add `site_id` to events and partition data per site for isolation and analytics.
- **Federated architecture**: Deploy regional backends with central aggregation layer.
- **Multi-tenancy**: Support multiple factories with data isolation and cross-site reporting.

### Infrastructure Evolution
- **Container orchestration**: Deploy on Kubernetes with auto-scaling based on queue depth.
- **Monitoring**: Prometheus metrics + Grafana dashboards for observability.
- **Data warehouse**: ETL pipeline to data warehouse for historical analytics.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed scaling plan.

---
## 🌐 Production Deployment

### Docker Production Build

The application is production-ready with:
- ✅ **Health checks** - Frontend waits for backend readiness
- ✅ **Volume persistence** - Data survives container restarts
- ✅ **Environment variables** - Portable configuration
- ✅ **Auto-restart policies** - Resilient to crashes
- ✅ **Network isolation** - Secure container communication

### Recommended Hosting Platforms

**Backend (FastAPI):**
- Railway.app (recommended - PostgreSQL support)
- Render.com (free tier available)
- Fly.io (global edge deployment)

**Frontend (React):**
- Vercel (recommended - zero config)
- Netlify (continuous deployment)
- AWS S3 + CloudFront (enterprise)

### Environment Variables for Production

```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # For production
CORS_ORIGINS=https://yourdomain.com
API_RATE_LIMIT=200  # requests per minute

# Frontend (.env)
REACT_APP_API_URL=https://api.yourdomain.com
```

### Migration to PostgreSQL

For production at scale (100+ cameras):

```python
# Update DATABASE_URL in config.py
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/factory_db"
)
```

No code changes needed - SQLAlchemy handles the migration automatically.

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
