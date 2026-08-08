"use client";
import { motion } from "framer-motion";
import { Siren, ShieldAlert, AlertTriangle } from "lucide-react";
import { EmergencyPriority } from "@/types/traffic";
import { cn } from "@/lib/utils";

interface EmergencyBannerProps {
  priority: EmergencyPriority;
}

export function EmergencyBanner({ priority }: EmergencyBannerProps) {
  if (priority === "LOW" || priority === "MODERATE") return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative overflow-hidden rounded-xl border border-red-500/40 bg-red-500/10 p-4"
    >
      {/* Animated scanline */}
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-red-500/5 to-transparent"
        animate={{ x: ["-100%", "200%"] }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
      />
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-500/20 border border-red-500/30 shrink-0">
          <Siren className="h-5 w-5 text-red-400 animate-pulse" />
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-sm font-bold text-red-300 uppercase tracking-wide">
              {priority === "CRITICAL" ? "CRITICAL EMERGENCY OVERRIDE" : "HIGH EMERGENCY ALERT"}
            </span>
            <span className="h-2 w-2 rounded-full bg-red-400 animate-pulse" />
          </div>
          <p className="text-xs text-red-400/80">
            {priority === "CRITICAL"
              ? "Emergency vehicle detected — All signals overridden. Priority route activated."
              : "Emergency vehicles in zone — Priority signal timing engaged."}
          </p>
        </div>
        <ShieldAlert className="h-5 w-5 text-red-400 shrink-0" />
      </div>
      <div className="mt-3 flex items-center gap-4">
        <Badge label="Priority Route Activated" active />
        <Badge label="Signal Override Enabled" active={priority === "CRITICAL"} />
      </div>
    </motion.div>
  );
}

function Badge({ label, active }: { label: string; active: boolean }) {
  return (
    <div
      className={cn(
        "flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium",
        active
          ? "border-red-500/40 bg-red-500/15 text-red-300"
          : "border-slate-700 bg-slate-800/50 text-slate-500"
      )}
    >
      <div className={cn("h-1.5 w-1.5 rounded-full", active ? "bg-red-400 animate-pulse" : "bg-slate-600")} />
      {label}
    </div>
  );
}
