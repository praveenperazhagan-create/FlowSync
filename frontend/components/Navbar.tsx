"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import { Activity, GitFork, Menu, X } from "lucide-react";
import { useState } from "react";
import { useBackendHealth } from "@/hooks/useBackendHealth";
import { cn } from "@/lib/utils";

const navLinks = [
  { label: "Home", href: "/" },
  { label: "Dashboard", href: "/dashboard" },
  { label: "Analytics", href: "/analytics" },
  { label: "About", href: "/about" },
];

export function Navbar() {
  const { isOnline } = useBackendHealth();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-slate-950/70 backdrop-blur-xl">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 shadow-lg shadow-cyan-500/25 group-hover:shadow-cyan-500/50 transition-shadow">
              <Activity className="h-4 w-4 text-white" />
              <div className="absolute inset-0 rounded-lg bg-gradient-to-br from-cyan-400/30 to-transparent" />
            </div>
            <span className="text-lg font-bold tracking-tight text-white">
              Flow<span className="text-cyan-400">Sync</span>
            </span>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="px-3 py-2 text-sm text-slate-400 hover:text-white rounded-md hover:bg-white/5 transition-all"
              >
                {link.label}
              </Link>
            ))}
            <a
              href="https://github.com"
              target="_blank"
              rel="noreferrer"
              className="ml-2 px-3 py-2 text-sm text-slate-400 hover:text-white rounded-md hover:bg-white/5 transition-all flex items-center gap-1.5"
            >
              <GitFork className="h-4 w-4" />
              GitHub
            </a>
          </nav>

          {/* Status Badge */}
          <div className="hidden md:flex items-center gap-3">
            <div
              className={cn(
                "flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-medium transition-all",
                isOnline === null
                  ? "border-slate-700 bg-slate-800/50 text-slate-400"
                  : isOnline
                  ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-400"
                  : "border-red-500/30 bg-red-500/10 text-red-400"
              )}
            >
              <span
                className={cn(
                  "h-2 w-2 rounded-full",
                  isOnline === null
                    ? "bg-slate-500 animate-pulse"
                    : isOnline
                    ? "bg-emerald-400 animate-pulse"
                    : "bg-red-400"
                )}
              />
              {isOnline === null
                ? "Checking..."
                : isOnline
                ? "Backend Online"
                : "Backend Offline"}
            </div>
          </div>

          {/* Mobile Menu Toggle */}
          <button
            className="md:hidden p-2 text-slate-400 hover:text-white"
            onClick={() => setMobileOpen(!mobileOpen)}
          >
            {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="md:hidden border-t border-white/5 bg-slate-950/95 px-4 py-3 space-y-1"
        >
          {navLinks.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="block px-3 py-2 text-sm text-slate-300 hover:text-white hover:bg-white/5 rounded-md"
              onClick={() => setMobileOpen(false)}
            >
              {link.label}
            </Link>
          ))}
          <div
            className={cn(
              "flex items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-medium w-fit mt-2",
              isOnline
                ? "border-emerald-500/30 bg-emerald-500/10 text-emerald-400"
                : "border-red-500/30 bg-red-500/10 text-red-400"
            )}
          >
            <span className={cn("h-2 w-2 rounded-full", isOnline ? "bg-emerald-400 animate-pulse" : "bg-red-400")} />
            {isOnline ? "Backend Online" : "Backend Offline"}
          </div>
        </motion.div>
      )}
    </header>
  );
}
