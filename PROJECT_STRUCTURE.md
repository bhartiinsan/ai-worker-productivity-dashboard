# Project Structure Guide

**Navigating the AI Worker Productivity Dashboard Codebase**

This document provides a map of the repository structure, file organization, and data flow. Use this as a reference when onboarding developers or understanding how components interact.

---

## 📁 High-Level Layout

```
ai-worker-productivity-dashboard/
├── backend/                    # FastAPI REST API + Business Logic
│   ├── app/                    # Application source code
│   │   ├── main.py            # FastAPI entry point, middleware setup
│   │   ├── database.py        # SQLAlchemy ORM configuration
│   │   ├── models.py          # Database table definitions (Worker, Workstation, AIEvent)
│   │   ├── schemas.py         # Pydantic validation schemas (request/response)
│   │   ├── routes.py          # API endpoint handlers (deprecated, use services/)
│   │   ├── crud.py            # Database CRUD operations
│   │   ├── config.py          # Environment and configuration management
│   │   ├── constants.py       # Application constants (shift times, thresholds)
│   │   ├── middleware.py      # Rate limiter and custom middleware
│   │   ├── seed_data.py       # Demo data generators
│   │   └── services/          # Business logic layer (RECOMMENDED ENTRY POINT)
│   │       ├── events_service.py         # Event ingestion with deduplication
│   │       ├── metrics_service.py        # Utilization, throughput calculations
│   │       └── seed_service.py           # Seeding logic
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Container image definition
│   └── .env.example           # Environment variables template
│
├── frontend/                   # React + TypeScript Dashboard
│   ├── public/                # Static assets (index.html, favicon)
│   ├── src/
│   │   ├── index.tsx          # React root component entry point
│   │   ├── App.tsx            # Main dashboard component with state management
│   │   ├── types.ts           # TypeScript interfaces (FactoryMetrics, WorkerMetrics, etc.)
│   │   ├── App.css            # Global styles
│   │   ├── index.css          # Tailwind base styles
│   │   └── services/
│   │       └── api.ts         # Axios client + API call wrappers (getWorkerMetrics, getFactoryMetrics)
│   ├── package.json           # Node.js dependencies
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── tsconfig.json          # TypeScript configuration
│   ├── Dockerfile            # Container image definition
│   └── nginx.conf            # Production reverse proxy config
│
├── docker-compose.yml         # Multi-container orchestration (backend + frontend)
├── README.md                  # Project overview and quick start
├── PROJECT_STRUCTURE.md       # THIS FILE
├── PULL_REQUEST_TEMPLATE.md   # GitHub PR workflow template
├── BACKEND.bat                # Windows batch script to start backend
├── FRONTEND.bat               # Windows batch script to start frontend
└── LAUNCH.bat                 # Windows batch script to start all services

```

---

## 🎯 Key Files by Purpose

### **Backend - Entry Points**

| File | Purpose | Key Functions |
|------|---------|---|
| `backend/app/main.py` | FastAPI app initialization | `app`, middleware setup, health checks |
| `backend/app/routes.py` | Legacy API endpoints | Deprecated; use services/ instead |

### **Backend - Data Layer**

| File | Purpose | Key Classes/Functions |
|------|---------|---|
| `backend/app/models.py` | SQLAlchemy ORM models | `Worker`, `Workstation`, `AIEvent` table definitions |
| `backend/app/database.py` | Database connection & session | `engine`, `SessionLocal`, `get_db()` |
| `backend/app/schemas.py` | Pydantic validation | `AIEventCreate`, `WorkerMetrics`, `FactoryMetrics` |
| `backend/app/crud.py` | Low-level CRUD operations | `get_worker()`, `create_ai_event()`, `get_events()` |

### **Backend - Business Logic** ⭐ **START HERE**

| File | Purpose | Key Functions |
|------|---------|---|
| `backend/app/services/events_service.py` | Event ingestion pipeline | `ingest_event()`, `ingest_batch()`, `fetch_events()` |
| `backend/app/services/metrics_service.py` | KPI calculations | `worker_metrics()`, `workstation_metrics()`, `factory_metrics()` |
| `backend/app/services/seed_service.py` | Demo data generation | `seed_database()` |

### **Frontend - Entry Points**

| File | Purpose | Key Components |
|------|---------|---|
| `frontend/src/index.tsx` | React root | `ReactDOM.render(App)` |
| `frontend/src/App.tsx` | Main dashboard | State management, metric fetching, UI layout |

### **Frontend - Services & Types**

| File | Purpose | Key Functions/Types |
|------|---------|---|
| `frontend/src/services/api.ts` | HTTP client | `getWorkerMetrics()`, `getFactoryMetrics()`, `seedDatabase()` |
| `frontend/src/types.ts` | TypeScript interfaces | `FactoryMetrics`, `WorkerMetrics`, `AIEvent` |

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ EDGE DEVICE (CCTV AI Cameras)                                   │
│ → Generates events: { timestamp, worker_id, event_type, ... }  │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTP POST /api/events or /api/events/batch
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ BACKEND API LAYER                                               │
│                                                                  │
│  FastAPI Route Handler                                          │
│    ├─ receives POST /api/events                                 │
│    └─ calls events_service.ingest_event()                       │
│                                                                  │
│  events_service.ingest_event()                                  │
│    ├─ validates worker/workstation exist (crud.get_worker)     │
│    ├─ checks for duplicates (crud.get_event_by_identity)       │
│    └─ on success: crud.create_ai_event()                        │
│                                                                  │
│  crud.create_ai_event()                                         │
│    └─ INSERT AIEvent record → SQLite/PostgreSQL                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                     ▲
                     │ Data persisted in DB
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ DATABASE LAYER (SQLite / PostgreSQL)                            │
│                                                                  │
│  Tables:                                                         │
│    ├─ Worker (id, name, location)                               │
│    ├─ Workstation (id, name, line)                              │
│    └─ AIEvent (timestamp, worker_id, event_type, confidence)   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                     ▲
                     │ GET /api/metrics/workers?worker_id=W1
                     │ calls metrics_service.worker_metrics()
                     │
┌─────────────────────────────────────────────────────────────────┐
│ METRICS COMPUTATION LAYER                                       │
│                                                                  │
│  metrics_service.worker_metrics()                               │
│    ├─ crud.get_events(db, worker_id='W1')                       │
│    ├─ _compute_durations()                                      │
│    │   ├─ sort events by timestamp (handle out-of-order)       │
│    │   ├─ calculate hours per state (working, idle, absent)    │
│    │   └─ return durations dict                                 │
│    ├─ compute utilization = working_h / elapsed_h * 100        │
│    ├─ compute units_per_hour = total_units / working_h         │
│    └─ return WorkerMetrics schema                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                     ▲
                     │ JSON response: { utilization_percentage, units_per_hour, ... }
                     │
┌─────────────────────────────────────────────────────────────────┐
│ FRONTEND DASHBOARD                                              │
│                                                                  │
│  React Component: App.tsx                                       │
│    ├─ useEffect → api.getWorkerMetrics()                        │
│    ├─ state: workers[], factory{}, workstations[]              │
│    ├─ Render KPI Cards                                          │
│    │   ├─ Factory utilization: {factory.utilization_percentage}│
│    │   ├─ Worker leaderboard: sorted by units_per_hour         │
│    │   └─ Workstation grid: occupancy heatmap                  │
│    └─ Real-time event stream (color-coded badges)              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
         ▲
         │ Browser displays charts + metrics
         │ Framer Motion animations
         │ Tailwind CSS styling
         │
    User sees Dashboard
```

---

## 🔍 Common Development Tasks

### Task: Add a New Metric (e.g., "Error Rate")

**Steps**:
1. Define schema in `backend/app/schemas.py`: add field to `WorkerMetrics`
2. Compute in `backend/app/services/metrics_service.py`: add logic to `worker_metrics()`
3. Add CRUD query in `backend/app/crud.py` if needed (e.g., `get_error_events()`)
4. Update API response in `backend/app/main.py` or routes
5. Update frontend type in `frontend/src/types.ts`: add field to `WorkerMetrics`
6. Render in `frontend/src/App.tsx`: display in KPI cards or charts

### Task: Add a New API Endpoint (e.g., `GET /api/metrics/trends`)

**Steps**:
1. Create service function in `backend/app/services/metrics_service.py`: `metric_trends(db, worker_id, days=7)`
2. Add route handler in `backend/app/main.py`:
   ```python
   @app.get("/api/metrics/trends")
   def get_trends(db: Session = Depends(get_db), worker_id: str = Query(...)):
       return metrics_service.metric_trends(db, worker_id)
   ```
3. Add API wrapper in `frontend/src/services/api.ts`: `export const getTrends = (workerId) => axios.get(...)`
4. Call from React in `frontend/src/App.tsx`: `const trends = await api.getTrends('W1')`
5. Render in UI components

### Task: Debug a Deduplication Issue

**Steps**:
1. Check database: `SELECT * FROM ai_events WHERE timestamp='2026-01-21T14:30:00' AND worker_id='W1'`
2. Check unique index in `backend/app/models.py`: `AIEvent` table constraints
3. Review `events_service.ingest_event()`: ensure dedup logic is correct
4. Check `crud.get_event_by_identity()`: SQL query for dedup lookup
5. Enable logging in `backend/app/main.py`: `logging.basicConfig(level=DEBUG)`

### Task: Improve Metric Performance

**Steps**:
1. Profile in `backend/app/services/metrics_service.py`: add timing logs
2. Optimize CRUD queries in `backend/app/crud.py`: add database indexes
3. Cache in-memory (Redis) if needed: wrap metrics_service functions
4. Test: measure response time before/after with `curl -w "@curl-format.txt"`

---

## 🧩 Component Interaction Matrix

| Component | Calls | Called By |
|-----------|-------|-----------|
| `main.py` | events_service, metrics_service, crud, database | FastAPI router |
| `events_service.py` | crud, schemas, database | main.py |
| `metrics_service.py` | crud, schemas | main.py |
| `crud.py` | database.engine, models | events_service, metrics_service |
| `database.py` | SQLAlchemy, models | crud, main.py |
| `models.py` | SQLAlchemy Base | database, crud |
| `App.tsx` | api.ts | Browser/React |
| `api.ts` | axios | App.tsx |

---

## 📋 Environment Variables

**Backend** (`.env`):
```
DATABASE_URL=sqlite:///./database.db  # or postgresql://...
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
API_RATE_LIMIT=100
```

**Frontend** (`.env`):
```
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 🚀 Local Development Workflow

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\Activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start

# Access
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

---

## 📞 Quick Reference: Who Owns What?

- **Data ingestion pipeline**: `backend/app/services/events_service.py`
- **Metric calculations**: `backend/app/services/metrics_service.py`
- **Database schema**: `backend/app/models.py`
- **API contracts**: `backend/app/schemas.py`
- **Frontend state**: `frontend/src/App.tsx`
- **HTTP client**: `frontend/src/services/api.ts`
- **TypeScript types**: `frontend/src/types.ts`

---

## ✅ Checklist: Starting a New Feature

- [ ] Read relevant service file(s) above
- [ ] Check existing tests (if any)
- [ ] Add feature to schema (backend/schemas.py or frontend/types.ts)
- [ ] Implement business logic (services/ layer)
- [ ] Add API endpoint (main.py)
- [ ] Wire frontend (App.tsx + api.ts)
- [ ] Test manually: http://localhost:8000/docs
- [ ] Commit with descriptive message
- [ ] Open PR (use PULL_REQUEST_TEMPLATE.md)
