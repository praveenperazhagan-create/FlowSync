import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(1)}%`;
}

export function getTrafficLevelColor(level: string): string {
  switch (level) {
    case "Low": return "text-emerald-400";
    case "Moderate": return "text-yellow-400";
    case "High": return "text-orange-400";
    case "Critical": return "text-red-500";
    default: return "text-slate-400";
  }
}

export function getTrafficLevelBg(level: string): string {
  switch (level) {
    case "Low": return "bg-emerald-500/20 border-emerald-500/40 text-emerald-300";
    case "Moderate": return "bg-yellow-500/20 border-yellow-500/40 text-yellow-300";
    case "High": return "bg-orange-500/20 border-orange-500/40 text-orange-300";
    case "Critical": return "bg-red-500/20 border-red-500/40 text-red-300";
    default: return "bg-slate-500/20 border-slate-500/40 text-slate-300";
  }
}

export function getEmergencyColor(priority: string): string {
  switch (priority) {
    case "LOW": return "bg-emerald-500/20 border-emerald-500/40 text-emerald-300";
    case "MODERATE": return "bg-yellow-500/20 border-yellow-500/40 text-yellow-300";
    case "HIGH": return "bg-orange-500/20 border-orange-500/40 text-orange-300";
    case "CRITICAL": return "bg-red-500/20 border-red-500/40 text-red-300";
    default: return "bg-slate-500/20 border-slate-500/40 text-slate-300";
  }
}

export function formatTimestamp(iso: string): string {
  return new Date(iso).toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}
