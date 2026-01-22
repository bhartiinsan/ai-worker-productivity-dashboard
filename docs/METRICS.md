# 📊 Metric Definitions & Formulas

Complete reference for all productivity metrics tracked by the AI Worker Productivity Dashboard.

**Context:** This system tracks 6 workers across 6 workstations using AI-generated CCTV events.

---

## Core Assumptions

All metric calculations are based on these fundamental assumptions:

1. **Time between two consecutive state events represents the duration of the earlier state.**
2. **If no new event is received, the last known state is assumed to continue.**
3. **`product_count` events are instantaneous and independent of time-based states.**
4. **Events are processed in timestamp order, regardless of arrival order.**

---

## Worker Metrics

### Worker Active Time
Sum of time intervals where the latest state event is `working`.

```
Active Time = Σ duration(event_type = "working")
```

### Worker Idle Time
Sum of time intervals where the latest state event is `idle`.

```
Idle Time = Σ duration(event_type = "idle")
```

### Utilization Percentage
Measures the percentage of observed time a worker spends actively working.

```
Utilization % = Active Time / (Active Time + Idle Time) × 100

Where:
  Active Time = Σ duration(event_type = "working")
  Idle Time = Σ duration(event_type = "idle")
  Range: 0-100%
```

**Interpretation**:
- **0-40%**: Low productivity, investigate for issues
- **40-70%**: Normal range, includes breaks and transitions
- **70-100%**: High productivity, verify sustainability

---

### Production Rate (Throughput)
Measures units produced per hour of active working time.

```
Units per Hour = Total Units Produced / Total Active Hours

Where:
  Total Units Produced = Σ count(event_type = "product_count")
  Total Active Hours = Active Time / 3600 (seconds to hours)
  Range: 0-∞ (typical: 2-8 units/hr)
```

**Industry Benchmarks**:
- Manual assembly: 2-4 units/hr
- Semi-automated: 4-6 units/hr
- Fully automated: 6+ units/hr

---

### Availability
Percentage of scheduled time the worker is present (not absent).

```
Availability % = (1 - Absent Time / Total Time) × 100

Where:
  Absent Time = Σ duration(event_type = "absent")
```

---

## Factory Metrics

### Average Utilization
Weighted average of worker utilization across the factory floor.

```
Factory Utilization = Σ(Worker Utilization × Worker Active Hours) / Σ(Total Active Hours)

Weighted by worker activity to avoid bias from idle workers
```

**Why Weighted?**
- Prevents workers with zero activity from pulling average down
- Reflects true operational capacity
- More accurate for shift-based operations

---

### Production Rate
Total factory output per hour of aggregate working time.

```
Factory Production Rate = Total Units / Total Working Hours (all workers)
```

---

## Workstation Metrics

### Occupancy
Percentage of time a workstation has an active worker assigned.

```
Occupancy % = (Time with Active Worker / Total Time) × 100
```

**Use Cases**:
- Identify underutilized equipment
- Optimize workstation allocation
- Justify new equipment purchases

---

### Efficiency
Units produced per hour of workstation occupancy.

```
Efficiency = Units Produced at Station / Occupancy Time
```

**Comparison to Worker Throughput**:
- Worker throughput includes all working time
- Station efficiency only counts time at that specific station
- Useful for bottleneck analysis

---

## Event Handling Guarantees

### Duplicate Events
Events are idempotent using a composite key of **(timestamp, worker_id, workstation_id, event_type)**. Duplicate events are ignored at ingestion via database UNIQUE constraint.

**Impact on metrics:** No double-counting possible.

### Out-of-Order Timestamps
Events are sorted by timestamp during metric aggregation. Late-arriving events are reprocessed during aggregation queries.

**Impact on metrics:** Calculations remain correct regardless of arrival order.

### Intermittent Connectivity
The backend assumes eventual consistency. Events can be ingested in batches once connectivity resumes without affecting correctness.

**Impact on metrics:** Historical data is retroactively correct when delayed events arrive.

---

## Calculation Notes

### Time Duration Computation
All durations are calculated from sequential events:
1. Events sorted by timestamp (ascending)
2. Duration = next_event.timestamp - current_event.timestamp
3. Last event assumes 5-minute default duration (configurable)

### Data Freshness
- Metrics recalculated every 5 seconds (live mode)
- Historical metrics cached for 1 minute
- Event aggregation uses SQL windowing functions for performance

### Null Handling
- Missing data returns `0` rather than `null`
- Workers with no events excluded from factory averages
- Empty datasets return `{"utilization": 0, "production_rate": 0}`

---

## API Response Format

```json
{
  "worker_id": 123,
  "metrics": {
    "utilization_percent": 67.2,
    "production_rate": 3.8,
    "availability_percent": 95.0
  },
  "time_range": {
    "start": "2026-01-21T08:00:00Z",
    "end": "2026-01-21T16:00:00Z"
  }
}
```

---

## Model Lifecycle Considerations

### Model Versioning
Each event payload can include a `model_version` field to track which CV model generated the event. This enables:
- Comparison of metrics across model versions
- Correlation of confidence scores with model updates
- A/B testing of new detection algorithms

### Drift Detection
Monitor these metrics over time to detect model degradation:
- Decreasing average confidence scores
- Changing idle/working ratio distributions
- Declining production rates without operational changes

### Retraining Triggers
Automatic retraining can be triggered when:
- Sustained confidence degradation is detected (e.g., 7-day moving average drops below threshold)
- Significant deviation from historical productivity baselines occurs (e.g., >2 standard deviations)
- Manual review flags systematic misclassifications

---

## Scalability Considerations

### Current Implementation (6 cameras)
- SQLite for simplicity
- In-memory aggregation
- 5-second refresh rate

### Scaling to 100+ Cameras
- **Database:** Migrate to PostgreSQL + TimescaleDB for time-series optimization
- **Ingestion:** Add Kafka/SQS message queue between cameras and backend
- **Indexing:** Composite indexes on (timestamp, worker_id, workstation_id)
- **Caching:** Redis for frequently accessed metrics

### Multi-Site Factories
- Add `site_id` field to events table
- Partition data by site for isolation
- Aggregate cross-site metrics in separate service

---

## Further Reading
- [Architecture Documentation](./ARCHITECTURE.md) - How metrics are computed
- [Edge Case Handling](./EDGE-CASES.md) - Data integrity strategies
- [Configuration Guide](./CONFIGURATION.md) - Threshold settings
- [README](../README.md) - Complete system overview
