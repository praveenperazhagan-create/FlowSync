"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Navbar } from "@/components/Navbar";
import { Sidebar } from "@/components/Sidebar";
import { useBackendHealth } from "@/hooks/useBackendHealth";
import {
  Settings as SettingsIcon,
  User,
  Bell,
  Sliders,
  Cpu,
  Server,
  Shield,
  LogOut,
  CheckCircle2,
  AlertCircle
} from "lucide-react";
import { toast } from "sonner";
import Link from "next/link";

export default function SettingsPage() {
  const { isOnline } = useBackendHealth();
  const [profile, setProfile] = useState({
    name: "Officer Alex Mercer",
    email: "alex.mercer@flowsync.city",
    role: "Senior Traffic Operations Controller",
    zone: "Downtown Central"
  });

  const [theme, setTheme] = useState<"dark" | "light" | "system">("dark");
  const [notifications, setNotifications] = useState(true);
  const [apiBase, setApiBase] = useState("http://localhost:8000");

  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success("User Profile updated successfully!");
  };

  return (
    <div className="min-h-screen bg-slate-950">
      <Navbar />

      <div className="flex pt-16">
        <Sidebar />

        <main className="flex-1 min-w-0 p-4 sm:p-6 lg:p-8 space-y-6">
          {/* Header */}
          <div>
            <div className="flex items-center gap-2 mb-1">
              <SettingsIcon className="h-5 w-5 text-cyan-400" />
              <h1 className="text-xl font-bold text-white">System Settings & Configuration</h1>
            </div>
            <p className="text-xs text-slate-400">
              Manage user profile, system preferences, AI model status, and backend connectivity
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left — Profile & Preferences */}
            <div className="lg:col-span-2 space-y-6">
              {/* User Profile Card */}
              <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-6 space-y-4">
                <div className="flex items-center gap-2 border-b border-white/10 pb-3">
                  <User className="h-4 w-4 text-cyan-400" />
                  <h2 className="text-sm font-bold text-white">User Profile</h2>
                </div>

                <form onSubmit={handleSaveProfile} className="space-y-4 text-xs">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-slate-400 font-semibold mb-1">Full Name</label>
                      <input
                        type="text"
                        value={profile.name}
                        onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                        className="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
                      />
                    </div>

                    <div>
                      <label className="block text-slate-400 font-semibold mb-1">Email Address</label>
                      <input
                        type="email"
                        value={profile.email}
                        onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                        className="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
                      />
                    </div>

                    <div>
                      <label className="block text-slate-400 font-semibold mb-1">Role Title</label>
                      <input
                        type="text"
                        value={profile.role}
                        onChange={(e) => setProfile({ ...profile, role: e.target.value })}
                        className="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
                      />
                    </div>

                    <div>
                      <label className="block text-slate-400 font-semibold mb-1">Assigned Zone</label>
                      <input
                        type="text"
                        value={profile.zone}
                        onChange={(e) => setProfile({ ...profile, zone: e.target.value })}
                        className="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
                      />
                    </div>
                  </div>

                  <button
                    type="submit"
                    className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 font-semibold text-white rounded-xl shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40 transition-all"
                  >
                    Save Profile Changes
                  </button>
                </form>
              </div>

              {/* Preferences */}
              <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-6 space-y-4">
                <div className="flex items-center gap-2 border-b border-white/10 pb-3">
                  <Sliders className="h-4 w-4 text-purple-400" />
                  <h2 className="text-sm font-bold text-white">System Preferences & Theme</h2>
                </div>

                <div className="space-y-4 text-xs">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold text-white">UI Theme Preference</p>
                      <p className="text-slate-500">Dark Mode optimized for traffic control rooms</p>
                    </div>
                    <select
                      value={theme}
                      onChange={(e: any) => setTheme(e.target.value)}
                      className="bg-slate-950 border border-white/10 text-white rounded-xl px-3 py-1.5 focus:outline-none"
                    >
                      <option value="dark">Dark Mode (Default)</option>
                      <option value="light">Light Mode</option>
                      <option value="system">System Default</option>
                    </select>
                  </div>

                  <div className="flex items-center justify-between border-t border-white/5 pt-3">
                    <div>
                      <p className="font-semibold text-white">Emergency Push Notifications</p>
                      <p className="text-slate-500">Alerts when ambulances or fire trucks are detected</p>
                    </div>
                    <input
                      type="checkbox"
                      checked={notifications}
                      onChange={(e) => setNotifications(e.target.checked)}
                      className="h-4 w-4 rounded bg-slate-950 border-white/10 text-cyan-500 focus:ring-0"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Right — AI Model Info & System Status */}
            <div className="space-y-6">
              {/* Backend & AI Connection */}
              <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-6 space-y-4">
                <div className="flex items-center gap-2 border-b border-white/10 pb-3">
                  <Server className="h-4 w-4 text-emerald-400" />
                  <h2 className="text-sm font-bold text-white">Backend Connection</h2>
                </div>

                <div className="space-y-3 text-xs">
                  <div className="flex items-center justify-between p-3 rounded-xl border border-white/5 bg-slate-950">
                    <span className="text-slate-400">FastAPI Server Status</span>
                    <span className={`font-bold ${isOnline ? "text-emerald-400" : "text-red-400"}`}>
                      {isOnline ? "HEALTHY" : "DISCONNECTED"}
                    </span>
                  </div>

                  <div>
                    <label className="block text-slate-400 font-semibold mb-1">API Base URL</label>
                    <input
                      type="text"
                      value={apiBase}
                      onChange={(e) => setApiBase(e.target.value)}
                      className="w-full bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-white font-mono focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              {/* AI Model Information */}
              <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-6 space-y-3">
                <div className="flex items-center gap-2 border-b border-white/10 pb-3">
                  <Cpu className="h-4 w-4 text-cyan-400" />
                  <h2 className="text-sm font-bold text-white">AI Model Information</h2>
                </div>

                <div className="space-y-2 text-xs text-slate-300">
                  <p><strong className="text-slate-400">Object Detection:</strong> YOLOv8 Nano (`yolov8n.pt`)</p>
                  <p><strong className="text-slate-400">Traffic Prediction:</strong> Random Forest Classifier</p>
                  <p><strong className="text-slate-400">Model File:</strong> `models/traffic_model.pkl`</p>
                  <p><strong className="text-slate-400">Simulation Engine:</strong> Mathematical Webster Delay Model</p>
                  <p><strong className="text-slate-400">System Version:</strong> FlowSync City AI v2.0.0</p>
                </div>
              </div>

              {/* Sign Out Action */}
              <Link href="/auth/login" className="block">
                <button className="w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-red-500/30 bg-red-500/10 text-xs font-bold text-red-400 hover:bg-red-500/20 transition-all">
                  <LogOut className="h-4 w-4" />
                  Sign Out of Session
                </button>
              </Link>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
