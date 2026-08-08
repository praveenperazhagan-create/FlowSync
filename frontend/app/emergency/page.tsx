"use client";
import { motion } from "framer-motion";
import { Siren, ShieldAlert, AlertTriangle, Zap, Radio } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";

const protocols = [
  {
    icon: Siren,
    title: "Ambulance Detection",
    description: "YOLOv8 identifies ambulances in real-time. Green corridors are automatically cleared on detected routes.",
    color: "text-red-400",
    bg: "from-red-500/20 to-red-500/5",
    border: "border-red-500/20",
  },
  {
    icon: ShieldAlert,
    title: "Police Vehicle Priority",
    description: "Police cars and emergency responders receive immediate signal override to minimize response times.",
    color: "text-blue-400",
    bg: "from-blue-500/20 to-blue-500/5",
    border: "border-blue-500/20",
  },
  {
    icon: Zap,
    title: "Fire Truck Corridor",
    description: "Dedicated signal phasing activated across intersections to create unobstructed fire truck pathways.",
    color: "text-orange-400",
    bg: "from-orange-500/20 to-orange-500/5",
    border: "border-orange-500/20",
  },
  {
    icon: Radio,
    title: "Emergency Broadcast",
    description: "All detected emergencies are logged and broadcast to connected intersection controllers in < 200ms.",
    color: "text-purple-400",
    bg: "from-purple-500/20 to-purple-500/5",
    border: "border-purple-500/20",
  },
];

export default function EmergencyPage() {
  return (
    <div className="min-h-screen bg-slate-950">
      <Navbar />
      <div className="flex pt-16">
        <Sidebar />
        <main className="flex-1 min-w-0 p-4 sm:p-6 lg:p-8">
          {/* Header */}
          <motion.div initial={{ opacity: 0, y: -12 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
            <div className="flex items-center gap-2 mb-1">
              <Siren className="h-5 w-5 text-red-400" />
              <h1 className="text-xl font-bold text-white">Emergency Management</h1>
            </div>
            <p className="text-sm text-slate-500">
              Priority routing and signal override for emergency vehicles detected by AI.
            </p>
          </motion.div>

          {/* Alert Banner */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative overflow-hidden rounded-2xl border border-red-500/30 bg-gradient-to-r from-red-500/10 to-orange-500/5 p-6 mb-8"
          >
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-transparent via-red-500/5 to-transparent"
              animate={{ x: ["-100%", "200%"] }}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
            />
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-red-500/20 border border-red-500/30 shrink-0">
                <AlertTriangle className="h-6 w-6 text-red-400" />
              </div>
              <div>
                <p className="text-sm font-bold text-red-300 mb-1 flex items-center gap-2">
                  EMERGENCY VEHICLE DETECTION ACTIVE
                  <span className="h-2 w-2 rounded-full bg-red-400 animate-pulse" />
                </p>
                <p className="text-xs text-red-400/70">
                  When YOLO detects ambulance / fire truck / police vehicle, all connected signals are immediately overridden
                  and a priority corridor is activated.
                </p>
              </div>
            </div>
            <div className="mt-4 grid grid-cols-3 gap-3">
              {["Priority Route Activated", "Signal Override Enabled", "Broadcast Sent"].map((badge) => (
                <div
                  key={badge}
                  className="flex items-center gap-1.5 rounded-lg border border-red-500/20 bg-red-500/10 px-3 py-2 text-xs text-red-300"
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-red-400 animate-pulse shrink-0" />
                  {badge}
                </div>
              ))}
            </div>
          </motion.div>

          {/* Protocol Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {protocols.map((p, i) => {
              const Icon = p.icon;
              return (
                <motion.div
                  key={p.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.08 }}
                  whileHover={{ y: -3 }}
                  className={`rounded-2xl border ${p.border} bg-gradient-to-br ${p.bg} p-6`}
                >
                  <div className={`mb-4 flex h-10 w-10 items-center justify-center rounded-xl border ${p.border} bg-slate-900/60`}>
                    <Icon className={`h-5 w-5 ${p.color}`} />
                  </div>
                  <h3 className="text-sm font-semibold text-white mb-2">{p.title}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{p.description}</p>
                </motion.div>
              );
            })}
          </div>

          {/* Info */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="mt-6 rounded-xl border border-white/6 bg-slate-900/40 p-5 text-center"
          >
            <p className="text-xs text-slate-500">
              Emergency detection is automatic — run a traffic analysis from the{" "}
              <a href="/dashboard" className="text-cyan-400 hover:underline">Dashboard</a> and
              the system will automatically activate emergency protocols if vehicles are detected.
            </p>
          </motion.div>
        </main>
      </div>
    </div>
  );
}
