# 🛡️ Edge Case Handling

Comprehensive guide to data integrity, error handling, and edge case strategies in the AI Worker Productivity Dashboard.

---

## 1. Duplicate Events

### Problem
Network retries may send the same event multiple times, causing inflated metrics.

**Example**:
```
Event: {worker_id: 5, timestamp: "10:00:00", event_type: "working"}
Network timeout → retry → same event sent twice
Without deduplication: 2x working time recorded
```

### Solution
**Database-level UNIQUE constraint**:
```sql
CREATE UNIQUE INDEX idx_event_dedup 
ON events(timestamp, worker_id, event_type);
```

**API Behavior**:
- Duplicate events rejected at INSERT time (IGNORE ON CONFLICT)
- Returns `{"status": "duplicate", "message": "Event already recorded"}`
- Idempotent design: calling endpoint twice = same database state

**Code Location**: `backend/app/models.py` - Events table schema

**Test Case**:
```bash
# Send same event twice
curl -X POST http://localhost:8000/api/events \
  -d '{"worker_id": 5, "timestamp": "2026-01-21T10:00:00", "event_type": "working"}'

# Second call returns duplicate status (no error)
```

---

## 2. Out-of-Order Events

### Problem
Event with timestamp 10:05 arrives after event with timestamp 10:10 due to network delays.

**Example**:
```
Camera sends events: [10:10 working], [10:05 working], [10:15 idle]
Without sorting: Incorrect duration calculations
```

### Solution
**Chronological Processing**:
- All metric calculations sort events by `timestamp` (not `created_at`)
- State machine processes events in timestamp order
- Late-arriving events correctly update metrics on recalculation

**Code Location**: `backend/app/services/metrics_service.py` - `_compute_durations()`

**Implementation**:
```python
def _compute_durations(events):
    # Always sort by actual event time, not insertion time
    sorted_events = sorted(events, key=lambda e: e.timestamp)
    
    durations = []
    for i in range(len(sorted_events) - 1):
        duration = sorted_events[i+1].timestamp - sorted_events[i].timestamp
        durations.append({
            'event': sorted_events[i],
            'duration_seconds': duration.total_seconds()
        })
    return durations
```

**Example Result**:
```
Received: [10:10 working], [10:05 working], [10:15 idle]
Sorted to: [10:05 working], [10:10 working], [10:15 idle]
Correctly computes: 10 minutes working, then transition to idle
```

---

## 3. Intermittent Connectivity

### Problem
Camera loses WiFi for 15 minutes, events buffered locally but need reliable delivery.

**Production Scenario**:
```
10:00 AM - WiFi drops
10:00-10:15 AM - 150 events buffered on edge device
10:15 AM - Connection restored
Risk: Event loss or timestamp corruption
```

### Solution
**Multi-layer Resilience**:

1. **Edge Buffering**:
   - Local SQLite queue stores up to 10,000 events
   - Disk-backed queue survives device restarts
   - FIFO processing on reconnection

2. **Exponential Backoff**:
   - Retry intervals: 1s, 2s, 4s, 8s, 16s... up to 5min
   - Prevents server overload on mass reconnection
   - Circuit breaker after 10 consecutive failures

3. **Batch Upload**:
   - Uploads 100 events/batch via `/api/events/batch`
   - Reduces HTTP overhead (150 requests → 2 requests)
   - Atomic batch commits (all or nothing)

4. **Bitemporal Tracking**:
   ```json
   {
     "event_time": "2026-01-21T10:05:00Z",  // When event occurred
     "created_at": "2026-01-21T10:20:00Z"   // When API received it
   }
   ```
   - `event_time` used for all metric calculations
   - `created_at` used for latency monitoring

5. **Health Monitoring**:
   - Edge device pings `/health` every 30s
   - Backend alerts if no heartbeat for 2 minutes
   - Dashboard shows "Offline" status for disconnected cameras

### Production Example
```
10:00 AM - WiFi drops
10:00-10:15 AM - 150 events buffered locally
10:15:00 AM - Connection restored
10:15:05 AM - Batch 1 uploaded (events 1-100)
10:15:12 AM - Batch 2 uploaded (events 101-150)
Result: All events preserved with accurate timestamps
```

**Code Location**: `backend/app/main.py` - `/api/events/batch` endpoint

---

## 4. Missing or Incomplete Data

### Problem
Worker has no events for a time period (e.g., system downtime, camera malfunction).

**Example**:
```
Query: Worker 5 metrics for 8:00-16:00
Database: Only 2 events recorded (system restarted at 14:00)
Risk: Division by zero, null pointer exceptions
```

### Solution
**Defensive Programming**:

```python
def calculate_utilization(events):
    if not events:
        return {"utilization": 0, "message": "No data available"}
    
    total_time = (events[-1].timestamp - events[0].timestamp).total_seconds()
    if total_time == 0:
        return {"utilization": 0, "message": "Insufficient time range"}
    
    working_time = sum(e.duration for e in events if e.type == "working")
    return {"utilization": round(working_time / total_time * 100, 1)}
```

**Frontend Handling**:
- Displays "No data" badge instead of broken charts
- Shows last known good value with timestamp
- Alerts user when data gap exceeds 30 minutes

**Factory Average Exclusion**:
```python
# Don't include workers with zero data in factory average
active_workers = [w for w in workers if w.event_count > 0]
factory_avg = sum(w.utilization for w in active_workers) / len(active_workers)
```

**Code Location**: `backend/app/services/metrics_service.py` - `_safe_divide()`

---

## 5. Confidence Score Filtering

### Problem
AI model has low confidence on some detections (occlusions, poor lighting).

**Example**:
```json
{
  "worker_id": 5,
  "event_type": "working",
  "confidence": 0.42  // Very uncertain detection
}
```

### Solution
**Multi-threshold Strategy**:

1. **API Rejection**:
   - Events with `confidence < 0.7` rejected at ingestion
   - Returns `{"status": "rejected", "reason": "Low confidence"}`
   - Configurable via `MIN_CONFIDENCE_THRESHOLD` env var

2. **Frontend Filtering**:
   - Toggle to show/hide low-confidence events
   - Visual indicator (yellow border) for 0.7-0.8 range
   - Full opacity for 0.8+ confidence

3. **Model Health Monitoring**:
   - Alert if average confidence drops below 0.75 over 1 hour
   - Daily report shows confidence distribution
   - Triggers model retraining workflow

4. **Gradual Decay**:
   ```
   confidence ≥ 0.9: 100% weight
   confidence ≥ 0.8: 90% weight
   confidence ≥ 0.7: 70% weight
   confidence < 0.7: Rejected
   ```

**Code Location**: `backend/app/main.py` - Validation middleware

**Configuration**:
```env
MIN_CONFIDENCE_THRESHOLD=0.7
ALERT_CONFIDENCE_AVG=0.75
MODEL_RETRAIN_THRESHOLD=0.65
```

---

## Data Integrity Checklist

- [x] **Deduplication**: UNIQUE constraint on (timestamp, worker_id, event_type)
- [x] **Ordering**: All queries sort by timestamp ASC before processing
- [x] **Buffering**: Edge devices queue up to 10,000 events locally
- [x] **Retry Logic**: Exponential backoff with 5-minute max interval
- [x] **Null Safety**: All divisions check for zero denominators
- [x] **Confidence Filtering**: Reject events with confidence < 0.7
- [x] **Health Checks**: Edge devices ping every 30 seconds
- [x] **Batch Processing**: 100 events per API batch call
- [x] **Bitemporal Tracking**: event_time vs created_at separation
- [x] **Error Responses**: Idempotent APIs return descriptive status

---

## Testing Edge Cases

### Manual Test Suite
```bash
# 1. Duplicate event test
curl -X POST http://localhost:8000/api/events -d @duplicate_event.json
curl -X POST http://localhost:8000/api/events -d @duplicate_event.json
# Expected: Second returns status="duplicate"

# 2. Out-of-order test
curl -X POST http://localhost:8000/api/events -d '{"timestamp": "2026-01-21T10:10:00", ...}'
curl -X POST http://localhost:8000/api/events -d '{"timestamp": "2026-01-21T10:05:00", ...}'
# Expected: Metrics recalculate in correct chronological order

# 3. Low confidence test
curl -X POST http://localhost:8000/api/events -d '{"confidence": 0.5, ...}'
# Expected: 400 Bad Request - confidence below threshold
```

### Automated Tests
Located in `backend/tests/test_edge_cases.py`:
- `test_duplicate_event_idempotency()`
- `test_out_of_order_event_sorting()`
- `test_missing_data_zero_division()`
- `test_confidence_threshold_enforcement()`

---

## Further Reading
- [Metric Definitions](./METRICS.md) - How calculations handle edge cases
- [Architecture](./ARCHITECTURE.md) - System resilience design
- [Configuration](./CONFIGURATION.md) - Tuning threshold parameters
