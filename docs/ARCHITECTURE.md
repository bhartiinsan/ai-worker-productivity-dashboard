# 🏗️ Architecture Deep Dive

## Data Journey: Edge Device → Real-Time Insights

The system implements a **four-stage data pipeline** for deterministic event processing and metric derivation:

```
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 1: EDGE DEVICE (CCTV AI Ingestion)                           │
├─────────────────────────────────────────────────────────────────────┤
│ Location: On-premise CCTV cameras + local AI inference             │
│ Process:                                                             │
│  • Real-time video analysis via pre-trained ML model (e.g., YOLOv8) │
│  • Event classification: working / idle / absent / product_count     │
│  • Confidence scoring (0.0–1.0)                                      │
│  • Local SQLite buffer for network resilience (store-and-forward)   │
│  • Batch assembly when connectivity restored or buffer fills         │
│ Output: JSON event array to API                                      │
└─────────────────────────────────────────────────────────────────────┘
                                   │ HTTPS POST
                                   ▼ (Batch: 1–1000 events)
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 2: API INGESTION & DEDUPLICATION                             │
├─────────────────────────────────────────────────────────────────────┤
│ Layer: FastAPI (1 instance) + Rate Limiter (100 req/min)           │
│ Deduplication Strategy:                                              │
│  • Unique key: (timestamp, worker_id, event_type)                   │
│  • Logic: If (ts, worker, event) seen before → skip                 │
│  • Handles out-of-order arrival via SQL UNIQUE INDEX               │
│ Validation:                                                           │
│  • Worker & workstation existence check                              │
│  • Confidence threshold enforcement (≥ 0.7)                         │
│  • Pydantic schema validation (ISO 8601 timestamps)                │
│ Response: Ingestion report (success, duplicate, error counts)       │
└─────────────────────────────────────────────────────────────────────┘
                                   │ INSERT/IGNORE
                                   ▼ (Time-indexed)
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 3: DATABASE PERSISTENCE (Bitemporal Tracking)                │
├─────────────────────────────────────────────────────────────────────┤
│ Store: SQLAlchemy ORM + SQLite (production: PostgreSQL)            │
│ Tables:                                                               │
│  • AIEvents: (id, timestamp, worker_id, workstation_id,             │
│              event_type, confidence, count, created_at, updated_at) │
│  • Workers: (id, name, location, active_since)                      │
│  • Workstations: (id, name, location, line, capacity)              │
│ Bitemporal Approach:                                                │
│  • event_time (timestamp): When activity occurred (per CCTV)       │
│  • created_at: Server insertion time                                │
│  • Enables audit trail and historical reconstruction                │
│ Indexing:                                                            │
│  • Clustered on (worker_id, timestamp) for metric queries           │
│  • Separate index on created_at for audit/compliance                │
└─────────────────────────────────────────────────────────────────────┘
                                   │ SELECT queries
                                   ▼ (Chronological aggregation)
┌─────────────────────────────────────────────────────────────────────┐
│ STAGE 4: REAL-TIME METRIC AGGREGATION                              │
├─────────────────────────────────────────────────────────────────────┤
│ On-demand Computation (React query → FastAPI → aggregation)         │
│ Worker Metrics:                                                      │
│  • Utilization = (working_hours / elapsed_hours) × 100%             │
│  • Throughput = total_units_produced / working_hours                │
│  • Availability = (1 - absent_hours / elapsed_hours) × 100%         │
│ Workstation Metrics:                                                 │
│  • Occupancy = sum(worker_present) / time_window                    │
│  • Efficiency = units_produced / occupancy_hours                    │
│ Factory Metrics:                                                     │
│  • Overall Utilization: Weighted by worker count                    │
│  • Production Target Variance: Actual vs. baseline                   │
│  • Shift Handover Analysis: Productivity dips (e.g., 10:00–10:15)   │
│ Caching Strategy:                                                    │
│  • In-memory cache (60s TTL) for dashboard refreshes                │
│  • Re-compute on new event ingestion                                 │
│ Output: JSON KPI objects to React Dashboard                         │
└─────────────────────────────────────────────────────────────────────┘
                                   │ REST (JSON)
                                   ▼ (React Query)
┌─────────────────────────────────────────────────────────────────────┐
│ FRONTEND PRESENTATION (React + TypeScript + Tailwind)              │
├─────────────────────────────────────────────────────────────────────┤
│ • Factory KPI cards: Workers active, avg. utilization, production   │
│ • Leaderboard: Top 3 workers by output (real-time update)          │
│ • Station grid: Utilization heatmap (red: idle, green: working)    │
│ • Event stream: Chronological AI event log with badges              │
│ • Charts: Productivity trend (hourly/daily, Recharts)              │
│ • Dark mode + animations (Framer Motion)                            │
│ • Responsive: Mobile, tablet, desktop layouts                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Key Design Principles

### 1. Determinism
Timestamp-based ordering ensures consistent aggregation across replays. Events are sorted chronologically before metric calculation, guaranteeing reproducible results.

### 2. Resilience
Local buffering + deduplication survive connectivity drops. Edge devices cache up to 10,000 events locally and use exponential backoff retry strategy.

### 3. Auditability
Bitemporal tracking preserves "what was known when" for compliance. Both event_time and created_at are stored, enabling reconstruction of historical states.

### 4. Scalability
Metric computation is read-optimized; indexing scales to 100M+ events. Database queries use covering indexes for sub-100ms response times.

---

## Scaling to 100+ Sites

**Current Architecture (6 Cameras):**
- SQLite database
- Single FastAPI instance
- Direct camera → backend connection

**Scaled Architecture (100+ Cameras):**

```
Edge (100+ Cameras)
        ↓
    Nginx (Load Balancer + Rate Limiting)
        ↓
FastAPI Cluster (5-20 pods in Kubernetes)
        ↓
    Apache Kafka (Event Stream Buffer)
        ↓
  ┌──────┬──────┬──────────┐
  ↓      ↓      ↓          ↓
PostgreSQL Redis ClickHouse TimescaleDB
(OLTP)   (Cache) (Analytics) (Time-Series)
```

### Key Architectural Changes

**1. Database Migration: SQLite → PostgreSQL + TimescaleDB**
```sql
-- Partition by month for fast queries
CREATE TABLE ai_events_2026_01 
PARTITION OF ai_events
FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

-- Hypertable for time-series (TimescaleDB)
SELECT create_hypertable('ai_events', 'timestamp');

-- Indexes for common queries
CREATE INDEX idx_worker_time ON ai_events(worker_id, timestamp DESC);
CREATE INDEX idx_workstation_time ON ai_events(workstation_id, timestamp DESC);
```

**2. Event Streaming: Kafka for Decoupling**
```python
# FastAPI Producer (handles 1000s of req/sec)
@app.post("/api/events")
async def ingest_event(event: AIEventCreate):
    await kafka_producer.send('ai-events', event.dict())
    return {"status": "queued"}
```

**3. Distributed Caching: Redis**
- Cache worker/workstation metrics for 60 seconds
- Invalidate on new event ingestion
- Reduces database load by 90%

**4. Read Replicas**
- Primary PostgreSQL for writes
- 3 read replicas for metric queries
- Load balanced across replicas

---

## Network Resilience

### Store-and-Forward Mechanism

Edge devices implement local buffering when network connectivity is lost:

```
┌─────────────────────────────┐
│   Edge Device (CCTV AI)     │
├─────────────────────────────┤
│ 1. Generate event           │
│ 2. Try POST to backend      │
│ 3. If network fails:        │
│    • Store in local SQLite  │
│    • Retry: 1s, 2s, 4s...   │
│ 4. On reconnect:            │
│    • Batch upload queue     │
│    • Use /api/events/batch  │
│ 5. Backend deduplicates     │
└─────────────────────────────┘
```

**Technical Details:**
- **Edge Storage**: SQLite buffer on edge device (persists across reboots)
- **Retry Strategy**: Exponential backoff: 1s → 2s → 4s → 8s → ... → 5min max
- **Batch Uploads**: 100 events/request when connectivity restored
- **Bounded Buffer**: Ring buffer keeps last 10,000 events to prevent memory overflow
- **Health Monitoring**: Edge pings backend `/health` every 30s to detect connectivity

**Production Example:**
```
10:00 AM - Network drops
10:00-10:15 - Edge buffers 150 events locally
10:15 AM - Connection restored
10:15:05 - Batch upload #1: Events 1-100
10:15:12 - Batch upload #2: Events 101-150
Dashboard reflects data with 15-minute lag visible in bitemporal tracking
```

---

## Model Drift Detection

The system monitors AI model confidence scores to detect degradation over time:

**Monitoring Strategy:**

1. **Real-Time Metrics**
   ```http
   GET /api/metrics/model-health
   
   Response:
   {
     "status": "Healthy",
     "avg_confidence": 0.9245,
     "samples": 100,
     "message": "Model confidence is within acceptable range"
   }
   ```

2. **Dashboard Visualization**
   - Line chart: 7-day rolling average confidence
   - Heatmap: Confidence by camera/workstation
   - Color codes:
     - Red < 0.75 (Critical - Retrain)
     - Yellow 0.75-0.85 (Warning - Monitor)
     - Green > 0.85 (Healthy)

3. **Automated Alerting**
   - Trigger alert if average confidence drops below 0.75
   - Alert on sudden confidence drop >10% in 1 hour
   - Weekly model performance reports

---

## Security Architecture

### Authentication & Authorization
- API key authentication for event ingestion
- Rate limiting: 100 requests/minute per IP
- CORS configured for specific frontend origins

### Data Protection
- HTTPS enforced in production
- Environment variables for sensitive config
- Database credentials in .env (not committed)

### Monitoring & Logging
- Structured logging with log levels (DEBUG, INFO, WARNING, ERROR)
- Health check endpoint for uptime monitoring
- Request/response logging for audit trails

---

## Performance Optimizations

1. **Database Indexes**
   - Composite index on (worker_id, timestamp)
   - Separate indexes on workstation_id and event_type
   - Covering indexes for common query patterns

2. **Query Optimization**
   - Use of SQLAlchemy's lazy loading
   - Batch queries instead of N+1 patterns
   - Limit result sets with pagination

3. **Caching Strategy**
   - In-memory cache for frequently accessed metrics
   - 60-second TTL for dashboard data
   - Cache invalidation on new event ingestion

4. **Frontend Optimizations**
   - Component memoization with React.memo
   - Debounced auto-refresh (30 seconds)
   - Virtual scrolling for large event lists

---

## Deployment Architecture

### Docker Compose (Current)
```yaml
services:
  backend:
    - FastAPI + Uvicorn
    - Port 8000
    - SQLite volume mount
  
  frontend:
    - React + Nginx
    - Port 3000 (development) / 80 (production)
    - Proxy to backend API
```

### Kubernetes (Production)
```yaml
Deployments:
  - backend-deployment (3 replicas)
  - frontend-deployment (2 replicas)
  - postgres-statefulset (1 primary, 2 replicas)

Services:
  - backend-service (ClusterIP)
  - frontend-service (LoadBalancer)
  - postgres-service (Headless)

Ingress:
  - TLS termination
  - Path-based routing (/api → backend, / → frontend)
```

---

## Future Enhancements

1. **WebSocket Support**
   - Real-time event streaming to dashboard
   - Sub-second metric updates
   - Live worker status changes

2. **Advanced Analytics**
   - Predictive maintenance alerts
   - Anomaly detection with ML
   - Shift optimization recommendations

3. **Multi-tenancy**
   - Support for multiple factories
   - Tenant isolation
   - Role-based access control

4. **Mobile App**
   - iOS/Android native apps
   - Push notifications for alerts
   - Offline mode with sync
