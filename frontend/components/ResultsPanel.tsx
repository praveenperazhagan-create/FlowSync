"use client";
import { motion } from "framer-motion";
import {
  Car, Bike, Bus, Truck, Clock, TrendingDown, Timer, ShieldAlert, Gauge, Hash,
} from "lucide-react";
import { TrafficAnalysisResponse } from "@/types/traffic";
import { cn, getTrafficLevelBg, getEmergencyColor } from "@/lib/utils";
import { AnimatedCounter } from "./AnimatedCounter";

interface ResultsPanelProps {
  result: TrafficAnalysisResponse;
}

const OUTPUT_BASE = process.env.NEXT_PUBLIC_OUTPUT_BASE_URL || "http://localhost:8000/output";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.07 },
  },
};
const item = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0 },
};

export function ResultsPanel({ result }: ResultsPanelProps) {
  // Fix 2: backend returns "output/annotated_xxx.jpg" — strip the "output/" prefix
  // so the final URL is: http://localhost:8000/output/annotated_xxx.jpg (not double-prefixed)
  const annotatedUrl = result.annotated_image
    ? `${OUTPUT_BASE}/${result.annotated_image.replace(/^.*output\//, "")}`
    : null;

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="space-y-4"
    >
      {/* Traffic Level + Confidence */}
      <motion.div variants={item} className="grid grid-cols-2 gap-4">
        <GlassCard className="flex flex-col items-center justify-center py-6">
          <p className="text-xs text-slate-500 mb-2 uppercase tracking-widest">Traffic Level</p>
          <span
            className={cn(
              "text-2xl font-extrabold px-5 py-2 rounded-full border tracking-wide",
              getTrafficLevelBg(result.traffic_level)
            )}
          >
            {result.traffic_level}
          </span>
        </GlassCard>

        <GlassCard className="flex flex-col items-center justify-center py-6 gap-2">
          <p className="text-xs text-slate-500 uppercase tracking-widest">AI Confidence</p>
          <CircularProgress value={result.confidence} />
          <p className="text-xs text-slate-500">Model certainty</p>
        </GlassCard>
      </motion.div>

      {/* Vehicle Count Cards */}
      <motion.div variants={item} className="grid grid-cols-4 gap-3">
        {[
          { label: "Cars", value: result.cars || 0, Icon: Car, color: "text-cyan-400" },
          { label: "Bikes", value: result.bikes || 0, Icon: Bike, color: "text-purple-400" },
          { label: "Buses", value: result.buses || result.bus || 0, Icon: Bus, color: "text-blue-400" },
          { label: "Trucks", value: result.trucks || result.truck || 0, Icon: Truck, color: "text-orange-400" },
        ].map(({ label, value, Icon, color }) => (
          <GlassCard key={label} className="flex flex-col items-center gap-2 py-4">
            <Icon className={cn("h-5 w-5", color)} />
            <p className="text-xl font-bold text-white">
              <AnimatedCounter value={value} />
            </p>
            <p className="text-xs text-slate-500">{label}</p>
          </GlassCard>
        ))}
      </motion.div>

      {/* Signal Timing */}
      <motion.div variants={item} className="grid grid-cols-3 gap-3">
        {[
          { label: "Current", value: result.current_signal_time ?? 60, suffix: "s", Icon: Clock, color: "text-slate-400" },
          { label: "Recommended", value: result.recommended_signal_time, suffix: "s", Icon: Timer, color: "text-cyan-400" },
          {
            label: "Difference",
            value: (result.signal_difference ?? (result.recommended_signal_time - 60)) >= 0 
              ? `+${result.signal_difference ?? (result.recommended_signal_time - 60)}` 
              : result.signal_difference ?? (result.recommended_signal_time - 60),
            suffix: "s",
            Icon: Gauge,
            color: (result.signal_difference ?? (result.recommended_signal_time - 60)) > 0 ? "text-orange-400" : "text-emerald-400",
          },
        ].map(({ label, value, suffix, Icon, color }) => (
          <GlassCard key={label} className="flex flex-col items-center gap-2 py-5">
            <Icon className={cn("h-5 w-5", color)} />
            <p className={cn("text-2xl font-bold", color)}>{value}<span className="text-sm text-slate-500">{suffix}</span></p>
            <p className="text-xs text-slate-500">{label}</p>
          </GlassCard>
        ))}
      </motion.div>

      {/* Queue + Reductions */}
      <motion.div variants={item} className="grid grid-cols-3 gap-3">
        <GlassCard className="flex flex-col items-center gap-2 py-5">
          <Hash className="h-5 w-5 text-yellow-400" />
          <p className="text-2xl font-bold text-white">
            <AnimatedCounter value={result.estimated_queue_length ?? result.estimated_queue ?? 0} />
          </p>
          <p className="text-xs text-slate-500">Queue Length</p>
        </GlassCard>
        <GlassCard className="flex flex-col items-center gap-2 py-5">
          <TrendingDown className="h-5 w-5 text-emerald-400" />
          <p className="text-xl font-bold text-emerald-400">{result.expected_congestion_reduction || "25%"}</p>
          <p className="text-xs text-slate-500">Congestion ↓</p>
        </GlassCard>
        <GlassCard className="flex flex-col items-center gap-2 py-5">
          <TrendingDown className="h-5 w-5 text-blue-400" />
          <p className="text-xl font-bold text-blue-400">{result.expected_waiting_time_reduction || "30%"}</p>
          <p className="text-xs text-slate-500">Wait Time ↓</p>
        </GlassCard>
      </motion.div>

      {/* Emergency Priority */}
      <motion.div variants={item}>
        <GlassCard className="flex items-center justify-between px-5 py-4">
          <div className="flex items-center gap-3">
            <ShieldAlert className="h-5 w-5 text-orange-400" />
            <span className="text-sm font-medium text-white">Emergency Priority</span>
          </div>
          <span
            className={cn(
              "text-sm font-bold px-4 py-1.5 rounded-full border",
              getEmergencyColor(result.emergency_priority || (result.emergency_vehicle ? "CRITICAL" : "LOW"))
            )}
          >
            {result.emergency_priority || (result.emergency_vehicle ? "CRITICAL" : "LOW")}
          </span>
        </GlassCard>
      </motion.div>

      {/* Annotated Image */}
      {annotatedUrl && (
        <motion.div variants={item}>
          <GlassCard className="p-0 overflow-hidden">
            <div className="px-4 py-3 border-b border-white/5 flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
              <p className="text-sm font-medium text-white">YOLO Annotated Output</p>
            </div>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={annotatedUrl}
              alt="Annotated traffic"
              className="w-full max-h-64 object-cover"
              onError={(e) => {
                (e.currentTarget as HTMLImageElement).style.display = "none";
              }}
            />
          </GlassCard>
        </motion.div>
      )}

      {/* Reasons Timeline */}
      <motion.div variants={item}>
        <GlassCard>
          <p className="text-sm font-semibold text-white mb-4">AI Decision Reasoning</p>
          <div className="space-y-3">
            {(result.reason_list || result.reason || []).map((reason_item: string, i: number) => (
              <div key={i} className="flex gap-3">
                <div className="flex flex-col items-center">
                  <div className="h-2 w-2 mt-1 rounded-full bg-cyan-400 shrink-0" />
                  {i < (result.reason_list || result.reason || []).length - 1 && (
                    <div className="w-px flex-1 bg-white/5 mt-1" />
                  )}
                </div>
                <p className="text-xs text-slate-400 pb-3">{reason_item}</p>
              </div>
            ))}
          </div>
        </GlassCard>
      </motion.div>
    </motion.div>
  );
}

function GlassCard({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("rounded-xl border border-white/8 bg-slate-900/60 backdrop-blur-xl p-4", className)}>
      {children}
    </div>
  );
}

function CircularProgress({ value }: { value: number }) {
  const r = 28;
  const circumference = 2 * Math.PI * r;
  const dashOffset = circumference - (value / 100) * circumference;

  const color =
    value >= 80 ? "#10b981" : value >= 60 ? "#f59e0b" : value >= 40 ? "#f97316" : "#ef4444";

  return (
    <div className="relative flex items-center justify-center">
      <svg width="80" height="80" viewBox="0 0 72 72" className="-rotate-90">
        <circle cx="36" cy="36" r={r} fill="none" stroke="#1e293b" strokeWidth="6" />
        <motion.circle
          cx="36"
          cy="36"
          r={r}
          fill="none"
          stroke={color}
          strokeWidth="6"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: dashOffset }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </svg>
      <div className="absolute text-center">
        <p className="text-lg font-bold text-white">{Math.round(value)}</p>
        <p className="text-xs text-slate-500 -mt-1">%</p>
      </div>
    </div>
  );
}
