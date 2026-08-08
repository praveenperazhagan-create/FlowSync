"use client";
import Link from "next/link";
import { type Variants, motion } from "framer-motion";
import {
  Activity, ArrowRight, Upload, Cpu, Zap, Shield,
  Car, BarChart3, Brain, ChevronRight, UserPlus, LogIn
} from "lucide-react";
import { Navbar } from "@/components/Navbar";

const features = [
  {
    icon: Brain,
    title: "YOLOv8 Detection",
    description: "Real-time vehicle detection — cars, bikes, buses, trucks, emergency vehicles.",
    color: "from-cyan-500/20 to-cyan-500/5",
    border: "border-cyan-500/20",
    iconColor: "text-cyan-400",
  },
  {
    icon: BarChart3,
    title: "Congestion Prediction",
    description: "Random Forest ML model predicts congestion level with confidence scoring.",
    color: "from-blue-500/20 to-blue-500/5",
    border: "border-blue-500/20",
    iconColor: "text-blue-400",
  },
  {
    icon: Zap,
    title: "Signal Optimization",
    description: "AI decision engine recommends optimal green signal timing to reduce wait times.",
    color: "from-purple-500/20 to-purple-500/5",
    border: "border-purple-500/20",
    iconColor: "text-purple-400",
  },
  {
    icon: Shield,
    title: "Emergency Priority",
    description: "Automatic detection and priority routing for ambulances, fire trucks and police.",
    color: "from-red-500/20 to-red-500/5",
    border: "border-red-500/20",
    iconColor: "text-red-400",
  },
];

const stats = [
  { value: "98%", label: "Detection Accuracy", color: "text-cyan-400" },
  { value: "<1s", label: "Inference Time", color: "text-blue-400" },
  { value: "30%", label: "Avg Wait Reduction", color: "text-purple-400" },
  { value: "7", label: "Vehicle Classes", color: "text-orange-400" },
];

const container: Variants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } },
};
const fadeUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6 } },
};

export default function HomePage() {
  return (
    <div className="min-h-screen bg-slate-950 hero-grid">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-32 pb-24 px-4 sm:px-6 lg:px-8">
        {/* Gradient Orbs */}
        <div className="pointer-events-none absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -left-40 h-[600px] w-[600px] rounded-full bg-cyan-500/8 blur-[120px]" />
          <div className="absolute top-20 right-0 h-[400px] w-[400px] rounded-full bg-purple-500/8 blur-[100px]" />
          <div className="absolute bottom-0 left-1/2 h-[300px] w-[600px] -translate-x-1/2 rounded-full bg-blue-500/6 blur-[80px]" />
        </div>

        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="relative mx-auto max-w-5xl text-center"
        >
          {/* Badge */}
          <motion.div variants={fadeUp} className="mb-6 inline-flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/5 px-4 py-1.5">
            <Activity className="h-3.5 w-3.5 text-cyan-400" />
            <span className="text-xs font-medium text-cyan-300 tracking-wide">AI-Powered Smart Traffic System</span>
            <ChevronRight className="h-3 w-3 text-cyan-500/50" />
          </motion.div>

          {/* Title */}
          <motion.h1
            variants={fadeUp}
            className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.08] mb-6"
          >
            <span className="gradient-text">AI Powered</span>
            <br />
            <span className="text-white">Smart Traffic</span>
            <br />
            <span className="text-slate-300">Management</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p
            variants={fadeUp}
            className="mx-auto max-w-2xl text-lg text-slate-400 leading-relaxed mb-10"
          >
            Upload traffic images, detect congestion, optimize traffic signals and prioritize
            emergency vehicles using Artificial Intelligence.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div variants={fadeUp} className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/auth/register">
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                className="flex items-center gap-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 px-7 py-3.5 text-sm font-semibold text-white shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 transition-shadow"
              >
                <UserPlus className="h-4 w-4" />
                Get Started
                <ArrowRight className="h-4 w-4" />
              </motion.button>
            </Link>
            <Link href="/auth/login">
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                className="flex items-center gap-2.5 rounded-xl border border-white/10 bg-white/5 px-7 py-3.5 text-sm font-semibold text-white hover:bg-white/8 hover:border-white/20 transition-all"
              >
                <LogIn className="h-4 w-4" />
                Sign In
              </motion.button>
            </Link>
          </motion.div>

          {/* Stats Row */}
          <motion.div
            variants={fadeUp}
            className="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-3xl mx-auto"
          >
            {stats.map(({ value, label, color }) => (
              <div
                key={label}
                className="rounded-xl border border-white/6 bg-slate-900/60 backdrop-blur-xl px-4 py-5 text-center"
              >
                <p className={`text-3xl font-extrabold ${color}`}>{value}</p>
                <p className="text-xs text-slate-500 mt-1">{label}</p>
              </div>
            ))}
          </motion.div>

          {/* Animated Traffic Illustration */}
          <motion.div
            variants={fadeUp}
            className="mt-16 relative mx-auto max-w-3xl"
          >
            <div className="relative overflow-hidden rounded-2xl border border-white/8 bg-slate-900/80 backdrop-blur-2xl shadow-2xl p-8">
              {/* Simulated signal + road */}
              <div className="flex flex-col items-center gap-4">
                <div className="flex items-center gap-8 w-full justify-center">
                  {/* Road */}
                  <div className="flex-1 h-px bg-gradient-to-r from-transparent via-cyan-500/40 to-transparent" />

                  {/* Signal */}
                  <div className="flex flex-col gap-1.5 rounded-lg border border-white/10 bg-slate-800 px-2.5 py-3">
                    <SignalLight color="bg-red-500" active={false} />
                    <SignalLight color="bg-yellow-500" active={false} />
                    <SignalLight color="bg-emerald-500" active={true} pulse />
                  </div>

                  <div className="flex-1 h-px bg-gradient-to-r from-cyan-500/40 via-transparent to-transparent" />
                </div>

                {/* Moving cars */}
                <div className="w-full overflow-hidden">
                  <div className="flex gap-4 w-full">
                    {Array.from({ length: 4 }).map((_, i) => (
                      <motion.div
                        key={i}
                        initial={{ x: "-100%" }}
                        animate={{ x: "400%" }}
                        transition={{
                          duration: 4,
                          delay: i * 0.8,
                          repeat: Infinity,
                          ease: "linear",
                        }}
                        className="shrink-0"
                      >
                        <Car className={`h-5 w-5 ${i % 2 === 0 ? "text-cyan-400" : "text-purple-400"}`} />
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Live AI labels */}
                <div className="flex flex-wrap justify-center gap-2 mt-2">
                  {["YOLO Detection", "RF Prediction", "Signal Optimizer", "Emergency Monitor"].map((label) => (
                    <div
                      key={label}
                      className="flex items-center gap-1.5 rounded-full border border-cyan-500/20 bg-cyan-500/5 px-3 py-1"
                    >
                      <div className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-pulse" />
                      <span className="text-xs text-cyan-300">{label}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Glow effect */}
            <div className="absolute -inset-1 rounded-2xl bg-gradient-to-r from-cyan-500/10 via-blue-500/5 to-purple-500/10 blur-xl -z-10" />
          </motion.div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <p className="text-xs font-medium uppercase tracking-widest text-cyan-400 mb-3">Capabilities</p>
            <h2 className="text-3xl font-bold text-white">
              Everything you need for{" "}
              <span className="gradient-text">smart traffic management</span>
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {features.map((feature, i) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 24 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  whileHover={{ y: -4 }}
                  className={`relative overflow-hidden rounded-2xl border ${feature.border} bg-gradient-to-b ${feature.color} p-6`}
                >
                  <div className={`mb-4 flex h-10 w-10 items-center justify-center rounded-xl border ${feature.border} bg-slate-900/60`}>
                    <Icon className={`h-5 w-5 ${feature.iconColor}`} />
                  </div>
                  <h3 className="text-sm font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-xs text-slate-400 leading-relaxed">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Banner */}
      <section className="py-16 px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, scale: 0.97 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative overflow-hidden rounded-2xl border border-cyan-500/20 bg-gradient-to-r from-cyan-500/10 via-blue-500/10 to-purple-500/10 p-10 text-center"
          >
            <div className="pointer-events-none absolute inset-0">
              <div className="absolute top-0 left-1/4 h-32 w-32 rounded-full bg-cyan-500/15 blur-3xl" />
              <div className="absolute bottom-0 right-1/4 h-32 w-32 rounded-full bg-purple-500/15 blur-3xl" />
            </div>
            <Cpu className="mx-auto h-10 w-10 text-cyan-400 mb-4" />
            <h2 className="text-2xl font-bold text-white mb-3">Ready to analyze your traffic?</h2>
            <p className="text-slate-400 mb-6 text-sm">Upload a traffic camera frame and get instant AI analysis.</p>
            <Link href="/dashboard">
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 px-8 py-3 text-sm font-semibold text-white shadow-lg shadow-cyan-500/25"
              >
                <Upload className="h-4 w-4" />
                Open Dashboard
                <ArrowRight className="h-4 w-4" />
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/5 py-8 text-center">
        <p className="text-xs text-slate-600">
          © 2026 FlowSync — AI Smart Traffic Management &nbsp;|&nbsp; Built with YOLOv8 + Random Forest + FastAPI
        </p>
      </footer>
    </div>
  );
}

function SignalLight({ color, active, pulse }: { color: string; active: boolean; pulse?: boolean }) {
  return (
    <div
      className={`h-4 w-4 rounded-full transition-all ${active ? color : "bg-slate-700"} ${pulse && active ? "animate-pulse" : ""}`}
      style={{ boxShadow: active ? `0 0 8px 2px currentColor` : "none" }}
    />
  );
}
