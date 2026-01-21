import axios from "axios";
import { AIEvent, FactoryMetrics, SeedResponse, WorkerMetrics, WorkstationMetrics } from "../types";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        "Content-Type": "application/json"
    }
});

export const getFactoryMetrics = () => api.get<FactoryMetrics>("/api/metrics/factory");
export const getWorkerMetrics = () => api.get<WorkerMetrics[]>("/api/metrics/workers");
export const getWorkstationMetrics = () => api.get<WorkstationMetrics[]>("/api/metrics/workstations");
export const getEvents = (limit = 40) => api.get<AIEvent[]>("/api/events", { params: { limit } });
export const seedDatabase = (clearExisting = false, hoursBack = 24) =>
    api.post<SeedResponse>("/api/seed", undefined, { params: { clear_existing: clearExisting, hours_back: hoursBack } });

export const adminSeed = (clearExisting = false) =>
    api.post<SeedResponse>("/api/admin/seed", undefined, { params: { clear_existing: clearExisting } });

export type ApiClient = typeof api;
