"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { fetchHistory } from "@/services/api";
import { HistoryRecord } from "@/types/traffic";
import {
  History as HistoryIcon,
  Search,
  Download,
  Trash2,
  Eye,
  Filter,
  ChevronLeft,
  ChevronRight,
  FileSpreadsheet,
  AlertCircle
} from "lucide-react";
import { toast } from "sonner";

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryRecord[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [zoneFilter, setZoneFilter] = useState("ALL");
  const [levelFilter, setLevelFilter] = useState("ALL");
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedRecord, setSelectedRecord] = useState<HistoryRecord | null>(null);
  const itemsPerPage = 8;

  useEffect(() => {
    fetchHistory()
      .then((data) => setHistory(data))
      .catch(() => {
        // Fallback demo dataset if CSV is empty
        setHistory([
          {
            timestamp: "2026-08-07 22:15:00",
            city_zone: "Downtown Central",
            vehicle_count: 185,
            cars: 120,
            bikes: 45,
            bus: 12,
            truck: 8,
            weather: "Clear",
            visibility: 10.0,
            prediction: "High",
            confidence: 94.5,
            recommended_signal_time: 80,
            queue_length: 58,
            waiting_time: 32.5
          },
          {
            timestamp: "2026-08-07 21:40:00",
            city_zone: "Commercial Hub",
            vehicle_count: 92,
            cars: 60,
            bikes: 25,
            bus: 4,
            truck: 3,
            weather: "Rain",
            visibility: 6.5,
            prediction: "Moderate",
            confidence: 96.2,
            recommended_signal_time: 60,
            queue_length: 22,
            waiting_time: 18.0
          },
          {
            timestamp: "2026-08-07 20:10:00",
            city_zone: "Industrial Corridor",
            vehicle_count: 240,
            cars: 110,
            bikes: 50,
            bus: 30,
            truck: 50,
            weather: "Clear",
            visibility: 10.0,
            prediction: "Severe",
            confidence: 91.8,
            recommended_signal_time: 100,
            queue_length: 95,
            waiting_time: 48.0
          }
        ]);
      });
  }, []);

  const handleDelete = (index: number) => {
    const updated = [...history];
    updated.splice(index, 1);
    setHistory(updated);
    toast.success("Log record deleted from view");
  };

  const handleExportCSV = () => {
    const headers = "timestamp,city_zone,vehicle_count,cars,bikes,bus,truck,weather,visibility,prediction,confidence,recommended_signal_time,queue_length,waiting_time\n";
    const rows = history.map(h => Object.values(h).join(",")).join("\n");
    const blob = new Blob([headers + rows], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Traffic_History_Export_${Date.now()}.csv`;
    a.click();
    toast.success("CSV Export Complete!");
  };

  // Filter & Search Logic
  const filteredHistory = history.filter((record) => {
    const matchesSearch =
      record.city_zone.toLowerCase().includes(searchTerm.toLowerCase()) ||
      record.prediction.toLowerCase().includes(searchTerm.toLowerCase()) ||
      record.timestamp.includes(searchTerm);
    const matchesZone = zoneFilter === "ALL" || record.city_zone === zoneFilter;
    const matchesLevel = levelFilter === "ALL" || record.prediction === levelFilter;
    return matchesSearch && matchesZone && matchesLevel;
  });

  // Pagination
  const totalPages = Math.ceil(filteredHistory.length / itemsPerPage) || 1;
  const paginatedHistory = filteredHistory.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  return (
    <div className="min-h-screen bg-slate-950">
      <Navbar />

      <div className="flex pt-16">
        <Sidebar />

        <main className="flex-1 min-w-0 p-4 sm:p-6 lg:p-8 space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <HistoryIcon className="h-5 w-5 text-cyan-400" />
                <h1 className="text-xl font-bold text-white">Traffic Analysis History</h1>
              </div>
              <p className="text-xs text-slate-400">
                Audit Log of past predictions, vehicle counts, and signal timing decisions
              </p>
            </div>

            <button
              onClick={handleExportCSV}
              className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-xs font-semibold text-cyan-300 hover:bg-cyan-500/20 transition-all"
            >
              <FileSpreadsheet className="h-3.5 w-3.5" /> Download Full CSV
            </button>
          </div>

          {/* Search & Filter Bar */}
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-4 flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="relative w-full md:w-80">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search timestamp, zone, level..."
                className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-white/10 rounded-xl text-xs text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500"
              />
            </div>

            <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
              <div className="flex items-center gap-2">
                <Filter className="h-3.5 w-3.5 text-slate-400" />
                <span className="text-xs text-slate-400">Zone:</span>
                <select
                  value={zoneFilter}
                  onChange={(e) => setZoneFilter(e.target.value)}
                  className="bg-slate-950 border border-white/10 rounded-xl text-xs text-white px-3 py-1.5 focus:outline-none"
                >
                  <option value="ALL">All Zones</option>
                  <option value="Downtown">Downtown Central</option>
                  <option value="Commercial">Commercial Hub</option>
                  <option value="Industrial">Industrial Corridor</option>
                </select>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-400">Level:</span>
                <select
                  value={levelFilter}
                  onChange={(e) => setLevelFilter(e.target.value)}
                  className="bg-slate-950 border border-white/10 rounded-xl text-xs text-white px-3 py-1.5 focus:outline-none"
                >
                  <option value="ALL">All Levels</option>
                  <option value="Low">Low</option>
                  <option value="Moderate">Moderate</option>
                  <option value="High">High</option>
                  <option value="Severe">Severe</option>
                </select>
              </div>
            </div>
          </div>

          {/* History Data Table */}
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 overflow-hidden shadow-2xl">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-white/10 bg-slate-950/80 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    <th className="py-3.5 px-4">Date & Time</th>
                    <th className="py-3.5 px-4">City Zone</th>
                    <th className="py-3.5 px-4">Vehicles</th>
                    <th className="py-3.5 px-4">Traffic Level</th>
                    <th className="py-3.5 px-4">Confidence</th>
                    <th className="py-3.5 px-4">Signal Time</th>
                    <th className="py-3.5 px-4">Queue</th>
                    <th className="py-3.5 px-4 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5 text-xs text-slate-300">
                  {paginatedHistory.length > 0 ? (
                    paginatedHistory.map((row, idx) => (
                      <tr key={idx} className="hover:bg-white/5 transition-colors">
                        <td className="py-3.5 px-4 font-mono text-slate-400">{row.timestamp}</td>
                        <td className="py-3.5 px-4 font-semibold text-white">{row.city_zone}</td>
                        <td className="py-3.5 px-4 font-mono text-cyan-400">{row.vehicle_count}</td>
                        <td className="py-3.5 px-4">
                          <span
                            className={`px-2.5 py-1 rounded-full text-[11px] font-semibold border ${
                              row.prediction === "Severe"
                                ? "bg-red-500/10 text-red-400 border-red-500/30"
                                : row.prediction === "High"
                                ? "bg-amber-500/10 text-amber-400 border-amber-500/30"
                                : row.prediction === "Moderate"
                                ? "bg-blue-500/10 text-blue-400 border-blue-500/30"
                                : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
                            }`}
                          >
                            {row.prediction}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 font-mono">{row.confidence}%</td>
                        <td className="py-3.5 px-4 font-bold text-purple-400">{row.recommended_signal_time}s</td>
                        <td className="py-3.5 px-4">{row.queue_length} veh</td>
                        <td className="py-3.5 px-4 text-right space-x-2">
                          <button
                            onClick={() => setSelectedRecord(row)}
                            className="p-1.5 rounded-lg border border-white/10 bg-slate-800 text-slate-300 hover:text-white hover:border-cyan-500 transition-all"
                            title="View Details"
                          >
                            <Eye className="h-3.5 w-3.5" />
                          </button>
                          <button
                            onClick={() => handleDelete(idx)}
                            className="p-1.5 rounded-lg border border-white/10 bg-slate-800 text-slate-400 hover:text-red-400 hover:border-red-500/40 transition-all"
                            title="Delete Record"
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={8} className="py-12 text-center text-slate-500 text-xs">
                        No traffic history logs found matching criteria.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Pagination Controls */}
            <div className="p-4 border-t border-white/10 bg-slate-950/60 flex items-center justify-between">
              <span className="text-xs text-slate-500">
                Page {currentPage} of {totalPages} ({filteredHistory.length} total entries)
              </span>

              <div className="flex items-center gap-2">
                <button
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  className="p-1.5 rounded-lg border border-white/10 bg-slate-900 text-slate-400 hover:text-white disabled:opacity-40"
                >
                  <ChevronLeft className="h-4 w-4" />
                </button>
                <button
                  disabled={currentPage >= totalPages}
                  onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                  className="p-1.5 rounded-lg border border-white/10 bg-slate-900 text-slate-400 hover:text-white disabled:opacity-40"
                >
                  <ChevronRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>

          {/* Record Details Modal */}
          {selectedRecord && (
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
              <div className="bg-slate-900 border border-white/10 rounded-2xl max-w-md w-full p-6 space-y-4">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <h3 className="text-sm font-bold text-white">Log Entry Detail</h3>
                  <button onClick={() => setSelectedRecord(null)} className="text-xs text-slate-400 hover:text-white">
                    ✕
                  </button>
                </div>

                <div className="space-y-2 text-xs">
                  <p><strong className="text-slate-400">Timestamp:</strong> {selectedRecord.timestamp}</p>
                  <p><strong className="text-slate-400">Zone:</strong> {selectedRecord.city_zone}</p>
                  <p><strong className="text-slate-400">Vehicle Count:</strong> {selectedRecord.vehicle_count} (Cars: {selectedRecord.cars}, Bikes: {selectedRecord.bikes}, Bus: {selectedRecord.bus}, Truck: {selectedRecord.truck})</p>
                  <p><strong className="text-slate-400">Weather & Visibility:</strong> {selectedRecord.weather} ({selectedRecord.visibility} km)</p>
                  <p><strong className="text-slate-400">Prediction:</strong> <span className="text-cyan-400">{selectedRecord.prediction}</span> ({selectedRecord.confidence}%)</p>
                  <p><strong className="text-slate-400">Recommended Signal Time:</strong> <span className="text-purple-400">{selectedRecord.recommended_signal_time} seconds</span></p>
                  <p><strong className="text-slate-400">Estimated Queue Length:</strong> {selectedRecord.queue_length} vehicles</p>
                  <p><strong className="text-slate-400">Estimated Delay:</strong> {selectedRecord.waiting_time}s</p>
                </div>

                <button
                  onClick={() => setSelectedRecord(null)}
                  className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-white rounded-xl"
                >
                  Close
                </button>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
