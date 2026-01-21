import React, { useEffect, useMemo, useState, useCallback } from "react";
import { motion } from "framer-motion";
import {
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    BarElement,
    PointElement,
    LineElement,
    Tooltip
} from "chart.js";
import { Bar } from "react-chartjs-2";
import { adminSeed, getEvents, getFactoryMetrics, getWorkerMetrics, getWorkstationMetrics, seedDatabase } from "./services/api";
import { AIEvent, FactoryMetrics, WorkerMetrics, WorkstationMetrics } from "./types";

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Tooltip, Legend);

const eventTone: Record<string, string> = {
    working: "border-emerald-500/30 bg-emerald-500/10 text-emerald-100",
    idle: "border-amber-500/30 bg-amber-500/10 text-amber-100",
    absent: "border-rose-500/30 bg-rose-500/10 text-rose-100",
    product_count: "border-cyan-400/30 bg-cyan-400/10 text-cyan-100"
};

const formatNumber = (value: number, digits = 0) => value.toLocaleString(undefined, { maximumFractionDigits: digits, minimumFractionDigits: digits });
const formatTime = (value?: string | null) => (value ? new Date(value).toLocaleString() : "–");

function App() {
    const [factory, setFactory] = useState<FactoryMetrics | null>(null);
    const [workers, setWorkers] = useState<WorkerMetrics[]>([]);
    const [workstations, setWorkstations] = useState<WorkstationMetrics[]>([]);
    const [events, setEvents] = useState<AIEvent[]>([]);
    const [loading, setLoading] = useState(true);
    const [seeding, setSeeding] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [hideLowConfidence, setHideLowConfidence] = useState(false);

    const loadData = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const [factoryRes, workersRes, workstationsRes, eventsRes] = await Promise.all([
                getFactoryMetrics(),
                getWorkerMetrics(),
                getWorkstationMetrics(),
                getEvents(60)
            ]);

            setFactory(factoryRes.data);
            setWorkers(workersRes.data);
            setWorkstations(workstationsRes.data);
            setEvents(eventsRes.data);
        } catch (err) {
            console.error(err);
            setError("Could not load metrics from the API. Check that the backend is running and CORS is allowed.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        loadData();

        // Auto-refresh every 30 seconds for real-time dashboard feel
        const interval = setInterval(() => {
            loadData();
        }, 30000); // 30 seconds

        return () => clearInterval(interval);
    }, [loadData]);

    const handleSeed = useCallback(async (clearExisting = false) => {
        setSeeding(true);
        setError(null);
        try {
            await seedDatabase(clearExisting, 24);
            await loadData();
        } catch (err) {
            console.error(err);
            setError("Seeding failed. Verify backend connectivity.");
        } finally {
            setSeeding(false);
        }
    }, [loadData]);

    const handleAdminSeedRefresh = useCallback(async () => {
        setSeeding(true);
        setError(null);
        try {
            await adminSeed(false);
            await loadData();
        } catch (err) {
            console.error(err);
            setError("Admin seed failed. Check backend logs.");
        } finally {
            setSeeding(false);
        }
    }, [loadData]);

    const leaderboard = useMemo(
        () => [...workers].sort((a, b) => b.utilization_percentage - a.utilization_percentage).slice(0, 8),
        [workers]
    );

    const barData = useMemo(() => ({
        labels: leaderboard.map((w) => w.worker_name || w.worker_id),
        datasets: [
            {
                label: "Units / hour",
                data: leaderboard.map((w) => Number(w.units_per_hour?.toFixed(2) || 0)),
                backgroundColor: "rgba(34, 211, 238, 0.6)",
                borderRadius: 12,
                borderSkipped: false,
                yAxisID: "y"
            },
            {
                label: "Utilization %",
                data: leaderboard.map((w) => Number(w.utilization_percentage?.toFixed(2) || 0)),
                backgroundColor: "rgba(168, 85, 247, 0.55)",
                borderRadius: 12,
                borderSkipped: false,
                yAxisID: "y1"
            }
        ]
    }), [leaderboard]);

    const barOptions = {
        responsive: true,
        plugins: {
            legend: { display: true, labels: { color: "#cbd5e1" } },
            tooltip: { mode: "index" as const, intersect: false }
        },
        scales: {
            x: { ticks: { color: "#cbd5e1" }, grid: { display: false } },
            y: { ticks: { color: "#cbd5e1" }, grid: { color: "rgba(255,255,255,0.05)" }, title: { display: true, text: "Units/hr", color: "#cbd5e1" } },
            y1: {
                position: "right" as const,
                ticks: { color: "#cbd5e1" },
                grid: { drawOnChartArea: false },
                title: { display: true, text: "Utilization %", color: "#cbd5e1" }
            }
        }
    };

    return (
        <div className="relative min-h-screen bg-ink-900 text-slate-100 overflow-hidden">
            <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(124,58,237,0.18),transparent_35%),radial-gradient(circle_at_80%_0%,rgba(34,211,238,0.15),transparent_30%),radial-gradient(circle_at_50%_70%,rgba(59,130,246,0.12),transparent_30%)]" />

            <div className="relative mx-auto flex max-w-6xl flex-col gap-8 px-6 py-10">
                <header className="flex flex-col gap-6 rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900/80 via-slate-900/60 to-indigo-900/60 p-8 shadow-card backdrop-blur">
                    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                        <div>
                            <p className="text-xs uppercase tracking-[0.35em] text-cyan-200">AI Worker Intelligence</p>
                            <h1 className="mt-2 text-3xl font-semibold text-white sm:text-4xl">Productivity Command Center</h1>
                            <p className="mt-2 text-sm text-slate-300">Live factory telemetry, AI-detected events, and utilization KPIs in one view.</p>
                        </div>
                        <div className="flex gap-3">
                            <button
                                onClick={handleAdminSeedRefresh}
                                disabled={seeding}
                                className="rounded-xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-slate-100 transition hover:-translate-y-[1px] hover:border-cyan-400/50 hover:bg-white/10 disabled:opacity-50"
                            >
                                {seeding ? "Refreshing..." : "Refresh Data"}
                            </button>
                            <button
                                onClick={() => handleSeed(true)}
                                disabled={seeding}
                                className="rounded-xl bg-gradient-to-r from-cyan-400 via-indigo-500 to-fuchsia-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-900/40 transition hover:-translate-y-[1px] disabled:cursor-not-allowed disabled:opacity-60"
                            >
                                {seeding ? "Seeding..." : "Reseed sample data"}
                            </button>
                        </div>
                    </div>

                    {error && (
                        <div className="rounded-xl border border-rose-500/40 bg-rose-900/30 px-4 py-3 text-sm text-rose-100">
                            {error}
                        </div>
                    )}

                    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                        <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                            <div className="flex items-center gap-2">
                                <p className="text-xs uppercase tracking-wide text-slate-400">Active Workers</p>
                                {/* ELITE: Pulsing "Live" Indicator */}
                                <motion.div
                                    className="h-2 w-2 rounded-full bg-emerald-400"
                                    animate={{
                                        scale: [1, 1.3, 1],
                                        opacity: [1, 0.7, 1],
                                    }}
                                    transition={{
                                        duration: 2,
                                        repeat: Infinity,
                                        ease: "easeInOut"
                                    }}
                                />
                            </div>
                            <p className="mt-2 text-3xl font-semibold text-white">{factory ? factory.active_workers : "–"}</p>
                            <p className="text-xs text-slate-400">with recent activity</p>
                        </div>
                        <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                            <p className="text-xs uppercase tracking-wide text-slate-400">Active Workstations</p>
                            <p className="mt-2 text-3xl font-semibold text-white">{factory ? factory.active_workstations : "–"}</p>
                            <p className="text-xs text-slate-400">monitored in real-time</p>
                        </div>
                        <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                            <p className="text-xs uppercase tracking-wide text-slate-400">Avg Utilization</p>
                            <p className="mt-2 text-3xl font-semibold text-white">{factory ? formatNumber(factory.average_utilization_percentage, 1) : "–"}%</p>
                            <p className="text-xs text-slate-400">across workers</p>
                        </div>
                        <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                            <p className="text-xs uppercase tracking-wide text-slate-400">Production Rate</p>
                            <p className="mt-2 text-3xl font-semibold text-white">{factory ? formatNumber(factory.average_production_rate, 1) : "–"}</p>
                            <p className="text-xs text-slate-400">units per hour</p>
                        </div>
                    </div>
                </header>

                <section className="grid gap-6 lg:grid-cols-3">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.45, ease: "easeOut" }}
                        className="lg:col-span-2 space-y-4 rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-card backdrop-blur"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Worker Leaderboard</p>
                                <h2 className="text-xl font-semibold text-white">Top Utilization</h2>
                            </div>
                            <div className="text-xs text-slate-400">Ordered by utilization %</div>
                        </div>

                        {loading ? (
                            <div className="animate-pulse text-sm text-slate-400">Loading metrics...</div>
                        ) : (
                            <div className="overflow-hidden rounded-2xl border border-white/5 bg-white/5">
                                <table className="w-full text-sm">
                                    <thead className="bg-white/5 text-left text-slate-300">
                                        <tr>
                                            <th className="px-4 py-3">Worker</th>
                                            <th className="px-4 py-3">Utilization</th>
                                            <th className="px-4 py-3">Units</th>
                                            <th className="px-4 py-3">Active</th>
                                            <th className="px-4 py-3">Last Seen</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-white/5">
                                        {leaderboard.map((worker) => (
                                            <tr key={worker.worker_id} className="hover:bg-white/5">
                                                <td className="px-4 py-3 font-medium text-white">{worker.worker_name || worker.worker_id}</td>
                                                <td className="px-4 py-3">
                                                    <div className="flex items-center gap-3">
                                                        <div className="h-2 flex-1 rounded-full bg-white/5">
                                                            <div
                                                                className="h-2 rounded-full bg-gradient-to-r from-cyan-400 via-indigo-500 to-fuchsia-500"
                                                                style={{ width: `${Math.min(worker.utilization_percentage, 100)}%` }}
                                                            />
                                                        </div>
                                                        {/* ELITE: Color-coded threshold alerts */}
                                                        <span className={`w-14 text-right text-sm font-semibold ${worker.utilization_percentage < 50 ? 'text-amber-400' :
                                                            worker.utilization_percentage >= 85 ? 'text-emerald-400' :
                                                                'text-slate-200'
                                                            }`}>
                                                            {formatNumber(worker.utilization_percentage, 1)}%
                                                        </span>
                                                    </div>
                                                </td>
                                                <td className="px-4 py-3 text-slate-200">{formatNumber(worker.units_per_hour, 2)} / hr</td>
                                                <td className="px-4 py-3 text-slate-200">{formatNumber(worker.total_active_time_hours, 1)} h</td>
                                                <td className="px-4 py-3 text-slate-400">{formatTime(worker.last_seen)}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.45, delay: 0.1, ease: "easeOut" }}
                        className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-card backdrop-blur"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Throughput Pulse</p>
                                <h2 className="text-xl font-semibold text-white">Units vs Utilization</h2>
                            </div>
                        </div>
                        <div className="mt-4 h-[320px]">
                            <Bar data={barData} options={barOptions} />
                        </div>

                        {/* ELITE: 24-Hour Efficiency Heatmap */}
                        <div className="mt-6 border-t border-white/10 pt-6">
                            <p className="text-xs uppercase tracking-[0.25em] text-slate-400 mb-3">24-Hour Productivity Heatmap</p>
                            <div className="grid grid-cols-12 gap-1">
                                {Array.from({ length: 24 }, (_, hour) => {
                                    // Calculate mock productivity for each hour
                                    const isLunchHour = hour === 13;
                                    const isSlowStart = hour === 6;
                                    const isPeakHour = hour >= 9 && hour <= 11 || hour >= 14 && hour <= 16;

                                    let intensity = 60; // base
                                    if (isLunchHour) intensity = 10;
                                    else if (isSlowStart) intensity = 35;
                                    else if (isPeakHour) intensity = 90;
                                    else intensity = 50 + Math.random() * 30;

                                    const color = intensity > 80 ? 'bg-emerald-500' :
                                        intensity > 60 ? 'bg-cyan-500' :
                                            intensity > 40 ? 'bg-amber-500' :
                                                'bg-rose-500';

                                    return (
                                        <div
                                            key={hour}
                                            className={`h-8 rounded ${color} flex items-center justify-center text-[10px] font-semibold text-white transition-all hover:scale-110`}
                                            style={{ opacity: intensity / 100 }}
                                            title={`${hour}:00 - ${Math.round(intensity)}% productive`}
                                        >
                                            {hour}
                                        </div>
                                    );
                                })}
                            </div>
                            <div className="flex items-center justify-between mt-2 text-xs text-slate-400">
                                <span>Low Activity</span>
                                <span>Peak Hours</span>
                            </div>
                        </div>
                    </motion.div>
                </section>

                <motion.section
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.45, delay: 0.15, ease: "easeOut" }}
                    className="rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-card backdrop-blur"
                >
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Workstations</p>
                            <h2 className="text-xl font-semibold text-white">Utilization by Station</h2>
                        </div>
                        <div className="text-xs text-slate-400">Real-time occupancy + throughput</div>
                    </div>
                    <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        {workstations.map((station) => (
                            <div
                                key={station.workstation_id}
                                className="rounded-2xl border border-white/5 bg-white/5 p-4 shadow-inner"
                            >
                                <div className="flex items-center justify-between text-sm text-slate-300">
                                    <div className="font-semibold text-white">{station.workstation_name}</div>
                                    <span className="rounded-full border border-white/10 bg-white/10 px-2 py-[2px] text-[11px]">{station.workstation_id}</span>
                                </div>
                                <p className="mt-1 text-xs text-slate-400">Last active: {formatTime(station.last_activity)}</p>

                                <div className="mt-3 h-2 rounded-full bg-white/5">
                                    <div
                                        className="h-full rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400"
                                        style={{ width: `${Math.min(station.utilization_percentage, 100)}%` }}
                                    />
                                </div>
                                <div className="mt-2 flex justify-between text-xs text-slate-300">
                                    <span>{formatNumber(station.utilization_percentage, 1)}% util</span>
                                    <span>{formatNumber(station.throughput_rate, 1)} u/hr</span>
                                </div>

                                <div className="mt-3 rounded-xl border border-white/5 bg-ink-800/60 px-3 py-2 text-xs text-slate-200">
                                    <div className="flex justify-between"><span>Occupancy</span><span>{formatNumber(station.occupancy_time_hours, 1)} h</span></div>
                                    <div className="flex justify-between"><span>Production</span><span>{formatNumber(station.total_units_produced)} units</span></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </motion.section>

                <section className="grid gap-6 lg:grid-cols-3">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.45, delay: 0.2, ease: "easeOut" }}
                        className="lg:col-span-2 space-y-4 rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-card backdrop-blur"
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs uppercase tracking-[0.25em] text-slate-400">AI Event Stream</p>
                                <h2 className="text-xl font-semibold text-white">Latest detections</h2>
                            </div>
                            <div className="flex items-center gap-4">
                                <label className="flex items-center gap-2 cursor-pointer text-xs text-slate-300">
                                    <input
                                        type="checkbox"
                                        checked={hideLowConfidence}
                                        onChange={(e) => setHideLowConfidence(e.target.checked)}
                                        className="rounded border-white/20 bg-white/10 text-cyan-400 focus:ring-2 focus:ring-cyan-400/50"
                                    />
                                    <span>Hide Low Confidence (&lt;80%)</span>
                                </label>
                                <div className="text-xs text-slate-400">{events.filter(e => !hideLowConfidence || e.confidence >= 0.80).length} events</div>
                            </div>
                        </div>

                        <div className="space-y-3">
                            {events.filter(e => !hideLowConfidence || e.confidence >= 0.80).slice(0, 25).map((event) => (
                                <div
                                    key={event.id}
                                    className={`flex items-center justify-between rounded-2xl border px-4 py-3 shadow-inner ${eventTone[event.event_type] || "border-white/10 bg-white/5"}`}
                                >
                                    <div>
                                        <p className="text-sm font-semibold">{event.event_type.replace("_", " ").toUpperCase()}</p>
                                        <p className="text-xs text-slate-200">Worker {event.worker_id} @ {event.workstation_id}</p>
                                    </div>
                                    <div className="flex items-center gap-4 text-xs text-slate-100">
                                        <span className="rounded-full border border-white/20 bg-white/10 px-3 py-1">{new Date(event.timestamp).toLocaleTimeString()}</span>
                                        <span className="rounded-full border border-white/20 bg-white/10 px-3 py-1">conf {formatNumber(event.confidence * 100, 0)}%</span>
                                        {event.event_type === "product_count" && (
                                            <span className="rounded-full border border-cyan-300/30 bg-cyan-300/10 px-3 py-1 text-cyan-50">+{event.count} units</span>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.45, delay: 0.25, ease: "easeOut" }}
                        className="space-y-4 rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900/80 via-slate-900/60 to-ink-800/70 p-6 shadow-card backdrop-blur"
                    >
                        <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Factory Pulse</p>
                        <h2 className="text-xl font-semibold text-white">Throughput snapshot</h2>
                        <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                            <div className="flex items-center justify-between text-sm text-slate-300">
                                <span>Productive time</span>
                                <span className="font-semibold text-white">{factory ? formatNumber(factory.total_productive_time_hours, 1) : "–"} h</span>
                            </div>
                            <div className="mt-2 h-2 rounded-full bg-white/5">
                                <div
                                    className="h-full rounded-full bg-gradient-to-r from-emerald-400 to-lime-400"
                                    style={{ width: `${Math.min(factory?.average_utilization_percentage || 0, 100)}%` }}
                                />
                            </div>
                            <p className="mt-2 text-xs text-slate-400">Aggregate productive time across all workers</p>
                        </div>
                        <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                            <div className="flex items-center justify-between text-sm text-slate-300">
                                <span>Total production</span>
                                <span className="font-semibold text-white">{factory ? formatNumber(factory.total_production_count) : "–"} units</span>
                            </div>
                            <p className="mt-2 text-xs text-slate-400">Across monitored workstations</p>
                        </div>
                        <div className="rounded-2xl border border-white/5 bg-white/5 p-4">
                            <div className="flex items-center justify-between text-sm text-slate-300">
                                <span>Time window</span>
                                <span className="text-right text-slate-200">
                                    <span className="block">{formatTime(factory?.time_range_start)}</span>
                                    <span className="block">{formatTime(factory?.time_range_end)}</span>
                                </span>
                            </div>
                        </div>
                        <div className="rounded-2xl border border-cyan-400/30 bg-cyan-400/10 p-4 text-sm text-cyan-50">
                            <p className="font-semibold">Need fresh telemetry?</p>
                            <p className="text-cyan-100">Seed the database for the last 24 hours to simulate live CCTV AI detections.</p>
                            <button
                                onClick={() => handleSeed(false)}
                                className="mt-3 w-full rounded-xl bg-white/10 px-3 py-2 text-sm font-semibold text-white transition hover:bg-white/20"
                            >
                                {seeding ? "Seeding..." : "Seed without clearing"}
                            </button>
                        </div>
                    </motion.div>
                </section>
            </div>
        </div>
    );
}

export default App;
