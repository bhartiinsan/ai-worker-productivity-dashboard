# 📊 Metric Definitions & Formulas

Complete reference for all productivity metrics tracked by the AI Worker Productivity Dashboard.

---

## Worker Metrics

### Utilization Percentage
Measures the percentage of observed time a worker spends actively working.

```
Utilization % = (Total Working Time / Total Observed Time) × 100

Where:
  Total Working Time = Σ duration(event_type = "working")
  Total Observed Time = (last_event_timestamp - first_event_timestamp)
  Range: 0-100%
```

**Interpretation**:
- **0-40%**: Low productivity, investigate for issues
- **40-70%**: Normal range, includes breaks and transitions
- **70-100%**: High productivity, verify sustainability

---

### Production Rate (Throughput)
Measures units produced per hour of working time.

```
Units per Hour = Total Units Produced / Total Working Time (hours)

Where:
  Total Units = Σ count(event_type = "product_count")
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

## Further Reading
- [Architecture Documentation](./ARCHITECTURE.md) - How metrics are computed
- [Edge Case Handling](./EDGE-CASES.md) - Data integrity strategies
- [Configuration Guide](./CONFIGURATION.md) - Threshold settings
