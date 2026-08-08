"use client";
import { motion } from "framer-motion";
import { Activity, Brain, Zap, GitFork, ExternalLink, Car } from "lucide-react";
import { Navbar } from "@/components/Navbar";
import Link from "next/link";

const timeline = [
  { step: "1", title: "Upload Image", desc: "Drag & drop or select a traffic camera frame (JPG, PNG, WebP)." },
  { step: "2", title: "YOLO Detection", desc: "YOLOv8 scans the image and counts cars, bikes, buses, trucks and emergency vehicles." },
  { step: "3", title: "Congestion Prediction", desc: "Random Forest ML model predicts traffic level: Low, Moderate, High, or Critical." },
  { step: "4", title: "Signal Decision", desc: "Decision engine calculates optimal green signal time and emergency priority." },
  { step: "5", title: "View Results", desc: "Interactive results with annotated image, charts, and AI reasoning." },
];

const techStack = [
  { label: "Next.js 15", desc: "React framework with App Router" },
  { label: "FastAPI", desc: "Python async backend" },
  { label: "YOLOv8", desc: "Real-time object detection" },
  { label: "Random Forest", desc: "Congestion classification" },
  { label: "Framer Motion", desc: "Fluid animations" },
  { label: "Recharts", desc: "Data visualizations" },
];

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-slate-950">
      <Navbar />
      <main className="pt-24 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <div className="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 shadow-xl shadow-cyan-500/30 mb-5">
              <Activity className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl font-extrabold text-white mb-3">
              About <span className="gradient-text">FlowSync</span>
            </h1>
            <p className="text-slate-400 max-w-xl mx-auto leading-relaxed">
              An AI-powered smart traffic management system designed to reduce congestion,
              optimize signal timing, and save lives with real-time emergency vehicle detection.
            </p>
          </motion.div>

          {/* How it works */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-12"
          >
            <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
              <Brain className="h-5 w-5 text-cyan-400" /> How It Works
            </h2>
            <div className="space-y-4">
              {timeline.map((t, i) => (
                <div key={t.step} className="flex gap-4">
                  <div className="flex flex-col items-center">
                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 text-xs font-bold text-white">
                      {t.step}
                    </div>
                    {i < timeline.length - 1 && <div className="mt-1 w-px flex-1 bg-cyan-500/10" />}
                  </div>
                  <div className="pb-4">
                    <p className="text-sm font-semibold text-white">{t.title}</p>
                    <p className="text-xs text-slate-400 mt-0.5">{t.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Tech Stack */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mb-12"
          >
            <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
              <Zap className="h-5 w-5 text-purple-400" /> Tech Stack
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {techStack.map(({ label, desc }) => (
                <div
                  key={label}
                  className="rounded-xl border border-white/8 bg-slate-900/60 p-4"
                >
                  <p className="text-sm font-semibold text-white">{label}</p>
                  <p className="text-xs text-slate-500 mt-0.5">{desc}</p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center gap-4 justify-center"
          >
            <Link href="/dashboard">
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20"
              >
                <Car className="h-4 w-4" />
                Try Dashboard
              </motion.button>
            </Link>
            <a href="https://github.com" target="_blank" rel="noreferrer">
              <motion.button
                whileHover={{ scale: 1.03 }}
                whileTap={{ scale: 0.97 }}
                className="flex items-center gap-2 rounded-xl border border-white/10 bg-white/5 px-6 py-3 text-sm font-semibold text-white hover:border-white/20 transition-all"
              >
                <GitFork className="h-4 w-4" />
                GitHub
                <ExternalLink className="h-3.5 w-3.5" />
              </motion.button>
            </a>
          </motion.div>
        </div>
      </main>
    </div>
  );
}
