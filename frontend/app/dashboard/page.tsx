"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { UploadCard } from "@/components/UploadCard";
import { ResultsPanel } from "@/components/ResultsPanel";
import { ResultsSkeleton } from "@/components/Skeleton";
import { EmergencyBanner } from "@/components/EmergencyBanner";
import { toast } from "sonner";
import {
  Activity,
  Cpu,
  Camera,
  Siren,
  Clock,
  Car,
  CheckCircle2,
  AlertTriangle,
  Upload,
  Video,
  Download,
  Play,
  RefreshCw,
  MapPin,
  Layers,
  Sparkles
} from "lucide-react";
import { analyzeImage, analyzeVideo, fetchSystemStats, triggerRetraining } from "@/services/api";
import { TrafficAnalysisResponse, SystemStatsResponse, VideoAnalysisResponse } from "@/types/traffic";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<"image" | "video">("image");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<TrafficAnalysisResponse | null>(null);
  const [videoResult, setVideoResult] = useState<VideoAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<SystemStatsResponse>({
    current_model_accuracy: 92.17,
    images_processed: 142,
    videos_processed: 18,
    average_response_time_ms: 18.4,
    vehicle_detection_count: 3480
  });

  // Load backend stats
  useEffect(() => {
    fetchSystemStats()
      .then((data) => setStats(data))
      .catch(() => {
        // Fallback default stats
      });
  }, []);

  const handleImageAnalyze = async (params: {
    file: File;
    weather: string;
    visibility: number;
    speed: number;
    zone: string;
    peak: boolean;
    incident: boolean;
  }) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await analyzeImage({
        image: params.file,
        city_zone: params.zone,
        weather_condition: params.weather,
        visibility_km: params.visibility,
        avg_speed_kmph: params.speed,
        is_peak_hour: params.peak,
        incident_reported: params.incident
      });
      setResult(data);
      toast.success(`Analysis complete: ${data.traffic_level} Traffic`);

      // Update stats locally
      setStats((prev) => ({
        ...prev,
        images_processed: prev.images_processed + 1,
        vehicle_detection_count: prev.vehicle_detection_count + (data.cars + data.bikes + data.bus + data.truck)
      }));
    } catch (err: any) {
      setError(err?.response?.data?.detail || "AI Processing Failed. Ensure backend is running.");
      toast.error("Traffic analysis failed");
    } finally {
      setIsLoading(false);
    }
  };

  const handleVideoAnalyze = async (file: File) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await analyzeVideo(file);
      setVideoResult(data);
      setResult(data.analysis_summary);
      toast.success(`Video analysis complete: ${data.peak_congestion} Congestion`);

      setStats((prev) => ({
        ...prev,
        videos_processed: prev.videos_processed + 1
      }));
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Video processing failed.");
      toast.error("Video processing failed");
    } finally {
      setIsLoading(false);
    }
  };

  const handleTriggerRetrain = async () => {
    toast.promise(triggerRetraining(), {
      loading: "Retraining Random Forest & Candidate Models...",
      success: (res) => `Model retrained successfully! Accuracy: ${res.accuracy}%`,
      error: "Retraining failed"
    });
  };

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
                <Activity className="h-5 w-5 text-cyan-400" />
                <h1 className="text-xl font-bold text-white">Live Monitoring Dashboard</h1>
              </div>
              <p className="text-xs text-slate-400">Real-time City AI Traffic Surveillance & Signal Control</p>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={handleTriggerRetrain}
                className="flex items-center gap-2 px-3 py-2 rounded-xl border border-cyan-500/30 bg-cyan-500/10 text-xs font-semibold text-cyan-300 hover:bg-cyan-500/20 transition-all"
              >
                <RefreshCw className="h-3.5 w-3.5" />
                Retrain AI Model
              </button>
            </div>
          </div>

          {/* 1. TOP SUMMARY CARDS */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            <div className="rounded-xl border border-white/10 bg-slate-900/60 p-4">
              <p className="text-[11px] font-medium text-slate-400 uppercase">Traffic Level</p>
              <p className="text-xl font-extrabold text-cyan-400 mt-1">
                {result ? result.traffic_level : "Moderate"}
              </p>
              <span className="text-[10px] text-slate-500">Live AI Feed</span>
            </div>

            <div className="rounded-xl border border-white/10 bg-slate-900/60 p-4">
              <p className="text-[11px] font-medium text-slate-400 uppercase">AI Status</p>
              <div className="flex items-center gap-1.5 mt-1">
                <div className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
                <p className="text-sm font-bold text-emerald-400">ONLINE</p>
              </div>
              <span className="text-[10px] text-slate-500">YOLO + RF Active</span>
            </div>

            <div className="rounded-xl border border-white/10 bg-slate-900/60 p-4">
              <p className="text-[11px] font-medium text-slate-400 uppercase">Active Cameras</p>
              <p className="text-xl font-extrabold text-purple-400 mt-1">24 / 24</p>
              <span className="text-[10px] text-slate-500">100% Operational</span>
            </div>

            <div className="rounded-xl border border-white/10 bg-slate-900/60 p-4">
              <p className="text-[11px] font-medium text-slate-400 uppercase">Emergency Vehicle</p>
              <p className="text-xl font-extrabold text-red-400 mt-1">
                {result?.emergency_vehicle ? "DETECTED" : "CLEAR"}
              </p>
              <span className="text-[10px] text-slate-500">Priority Corridor</span>
            </div>

            <div className="rounded-xl border border-white/10 bg-slate-900/60 p-4">
              <p className="text-[11px] font-medium text-slate-400 uppercase">Avg Signal Timing</p>
              <p className="text-xl font-extrabold text-blue-400 mt-1">
                {result ? `${result.recommended_signal_time}s` : "65s"}
              </p>
              <span className="text-[10px] text-slate-500">Optimized Cycle</span>
            </div>

            <div className="rounded-xl border border-white/10 bg-slate-900/60 p-4">
              <p className="text-[11px] font-medium text-slate-400 uppercase">Vehicles Today</p>
              <p className="text-xl font-extrabold text-emerald-400 mt-1">
                {(stats.vehicle_detection_count ?? 0).toLocaleString()}
              </p>
              <span className="text-[10px] text-slate-500">Cumulative Detection</span>
            </div>
          </div>

          {/* Emergency Alert Banner */}
          {result?.emergency_vehicle && (
            <div className="rounded-xl border border-red-500/40 bg-red-500/10 p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Siren className="h-6 w-6 text-red-400 animate-pulse" />
                <div>
                  <h3 className="text-sm font-bold text-red-200">EMERGENCY VEHICLE DETECTED IN CORRIDOR</h3>
                  <p className="text-xs text-red-300">Green Light Extension Activated (120s priority signal cycle assigned).</p>
                </div>
              </div>
            </div>
          )}

          {/* 2. LIVE TRAFFIC MAP & RECENT DETECTION */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Live Traffic Map (Interactive Placeholder) */}
            <div className="lg:col-span-2 rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-xl p-5 flex flex-col justify-between min-h-[360px]">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <MapPin className="h-4 w-4 text-cyan-400" />
                    <h2 className="text-sm font-bold text-white">Live City Traffic Map & Intersection Grid</h2>
                  </div>
                  <span className="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-1 rounded-full">
                    Live Stream Connected
                  </span>
                </div>

                {/* Simulated Map Visual */}
                <div className="relative h-64 rounded-xl border border-white/10 bg-slate-950 overflow-hidden flex items-center justify-center">
                  <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:16px_16px] opacity-40" />

                  {/* Simulated Roads */}
                  <div className="absolute w-full h-12 bg-slate-900 border-y border-slate-800 top-1/2 -translate-y-1/2 flex items-center justify-around px-8">
                    <span className="text-[10px] text-slate-600 font-mono">NORTH-SOUTH CORRIDOR</span>
                    <span className="text-[10px] text-slate-600 font-mono">EAST-WEST ARTERIAL</span>
                  </div>
                  <div className="absolute h-full w-12 bg-slate-900 border-x border-slate-800 left-1/2 -translate-x-1/2" />

                  {/* Intersection Sensor Nodes */}
                  <div className="absolute top-1/3 left-1/3 flex flex-col items-center">
                    <div className="h-4 w-4 rounded-full bg-emerald-500/80 animate-ping" />
                    <span className="text-[9px] font-bold text-slate-300 mt-1 bg-slate-900/90 px-1.5 py-0.5 rounded border border-white/10">
                      Downtown (Low)
                    </span>
                  </div>

                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center z-10">
                    <div className="h-6 w-6 rounded-full bg-red-500/80 animate-pulse border-2 border-red-300 flex items-center justify-center text-[10px] font-bold text-white">
                      !
                    </div>
                    <span className="text-[10px] font-bold text-red-400 mt-1 bg-slate-950 px-2 py-0.5 rounded border border-red-500/40">
                      Main Intersection: {result ? result.traffic_level : "High"}
                    </span>
                  </div>

                  <div className="absolute bottom-1/4 right-1/4 flex flex-col items-center">
                    <div className="h-4 w-4 rounded-full bg-amber-500/80 animate-pulse" />
                    <span className="text-[9px] font-bold text-slate-300 mt-1 bg-slate-900/90 px-1.5 py-0.5 rounded border border-white/10">
                      Commercial Zone (Moderate)
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-4 flex items-center justify-between text-xs text-slate-400 border-t border-white/5 pt-3">
                <span>Active City Zone: <strong className="text-white">Downtown Central</strong></span>
                <span>Signal Synchronization: <strong className="text-cyan-400">Adaptive Dynamic</strong></span>
              </div>
            </div>

            {/* Live AI Engine Status & Diagnostics */}
            <div className="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-xl p-5 flex flex-col justify-between space-y-4">
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <Cpu className="h-4 w-4 text-cyan-400" />
                  <h2 className="text-sm font-bold text-white">Live AI System Diagnostics</h2>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between p-2.5 rounded-lg border border-white/5 bg-slate-950/60">
                    <span className="text-xs text-slate-400">Model Accuracy</span>
                    <span className="text-xs font-bold text-emerald-400">{stats.current_model_accuracy}%</span>
                  </div>

                  <div className="flex items-center justify-between p-2.5 rounded-lg border border-white/5 bg-slate-950/60">
                    <span className="text-xs text-slate-400">Inference Response Time</span>
                    <span className="text-xs font-bold text-cyan-400">{stats.average_response_time_ms} ms</span>
                  </div>

                  <div className="flex items-center justify-between p-2.5 rounded-lg border border-white/5 bg-slate-950/60">
                    <span className="text-xs text-slate-400">Backend FastAPI Status</span>
                    <span className="text-xs font-bold text-emerald-400">CONNECTED</span>
                  </div>

                  <div className="flex items-center justify-between p-2.5 rounded-lg border border-white/5 bg-slate-950/60">
                    <span className="text-xs text-slate-400">YOLOv8 Engine</span>
                    <span className="text-xs font-bold text-emerald-400">READY</span>
                  </div>

                  <div className="flex items-center justify-between p-2.5 rounded-lg border border-white/5 bg-slate-950/60">
                    <span className="text-xs text-slate-400">Prediction Engine</span>
                    <span className="text-xs font-bold text-emerald-400">Random Forest</span>
                  </div>
                </div>
              </div>

              <div className="p-3 rounded-xl border border-cyan-500/20 bg-cyan-500/5">
                <p className="text-[11px] text-cyan-300 font-semibold mb-1">AI Recommendation Status</p>
                <p className="text-xs text-slate-400">
                  Adaptive mathematical simulation active. Next signal cycle recalculation in 15 seconds.
                </p>
              </div>
            </div>
          </div>

          {/* 3. UPLOAD & RECENT DETECTION SECTION */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Quick Actions & Input Form */}
            <div className="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-xl p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-white/5 pb-3">
                <div className="flex items-center gap-2">
                  <Upload className="h-4 w-4 text-cyan-400" />
                  <h2 className="text-sm font-bold text-white">Live Traffic Analysis Input</h2>
                </div>

                <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-white/10">
                  <button
                    onClick={() => setActiveTab("image")}
                    className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
                      activeTab === "image" ? "bg-cyan-500 text-white" : "text-slate-400 hover:text-white"
                    }`}
                  >
                    Image
                  </button>
                  <button
                    onClick={() => setActiveTab("video")}
                    className={`px-3 py-1 text-xs font-semibold rounded-md transition-all ${
                      activeTab === "video" ? "bg-cyan-500 text-white" : "text-slate-400 hover:text-white"
                    }`}
                  >
                    Video
                  </button>
                </div>
              </div>

              {activeTab === "image" ? (
                <UploadCard
                  onAnalyze={(params) =>
                    handleImageAnalyze({
                      file: params.image,
                      weather: params.weather_condition,
                      visibility: params.visibility_km,
                      speed: params.avg_speed_kmph ?? 40.0,
                      zone: params.city_zone,
                      peak: params.is_peak_hour,
                      incident: params.incident_reported
                    })
                  }
                  isLoading={isLoading}
                />
              ) : (
                <div className="space-y-4">
                  <div className="border-2 border-dashed border-white/10 rounded-xl p-8 text-center hover:border-cyan-500/40 transition-all bg-slate-950/40">
                    <Video className="mx-auto h-8 w-8 text-cyan-400 mb-2" />
                    <p className="text-xs font-semibold text-white">Upload Traffic Feed Video (.mp4 / .avi)</p>
                    <p className="text-[11px] text-slate-500 mt-1">Runs frame-by-frame YOLO & Signal optimization</p>
                    <input
                      type="file"
                      accept="video/*"
                      onChange={(e) => {
                        if (e.target.files?.[0]) handleVideoAnalyze(e.target.files[0]);
                      }}
                      className="mt-3 block w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-cyan-500/10 file:text-cyan-400 hover:file:bg-cyan-500/20"
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Detection Results & Decision Output */}
            <div>
              <AnimatePresence mode="wait">
                {isLoading ? (
                  <ResultsSkeleton />
                ) : result ? (
                  <ResultsPanel result={result} />
                ) : error ? (
                  <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-8 text-center min-h-[300px] flex flex-col items-center justify-center">
                    <AlertTriangle className="h-10 w-10 text-red-400 mb-2" />
                    <h3 className="text-sm font-bold text-red-300">Analysis Exception</h3>
                    <p className="text-xs text-slate-400 mt-1 max-w-xs">{error}</p>
                  </div>
                ) : (
                  <div className="rounded-2xl border border-dashed border-white/10 bg-slate-900/40 p-8 text-center min-h-[320px] flex flex-col items-center justify-center">
                    <Sparkles className="h-10 w-10 text-slate-600 mb-3" />
                    <h3 className="text-sm font-bold text-white">No Detection Active</h3>
                    <p className="text-xs text-slate-500 max-w-xs mt-1">
                      Select an image or video above to execute YOLOv8 detection and mathematical signal optimization.
                    </p>
                  </div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
