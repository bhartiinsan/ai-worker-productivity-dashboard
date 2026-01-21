export type EventType = "working" | "idle" | "absent" | "product_count";

export interface AIEvent {
    id: number;
    timestamp: string;
    worker_id: string;
    workstation_id: string;
    event_type: EventType;
    confidence: number;
    count: number;
    created_at: string;
}

export interface WorkerMetrics {
    worker_id: string;
    worker_name: string;
    total_active_time_hours: number;
    total_idle_time_hours: number;
    utilization_percentage: number;
    total_units_produced: number;
    units_per_hour: number;
    last_seen: string | null;
}

export interface WorkstationMetrics {
    workstation_id: string;
    workstation_name: string;
    occupancy_time_hours: number;
    utilization_percentage: number;
    total_units_produced: number;
    throughput_rate: number;
    last_activity: string | null;
}

export interface FactoryMetrics {
    total_productive_time_hours: number;
    total_production_count: number;
    average_utilization_percentage: number;
    average_production_rate: number;
    active_workers: number;
    active_workstations: number;
    time_range_start: string | null;
    time_range_end: string | null;
}

export interface SeedResponse {
    message: string;
    workers_created: number;
    workstations_created: number;
    events_created: number;
}
