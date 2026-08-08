"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  BarChart3,
  History,
  Settings,
  Activity,
  ChevronRight,
  LogOut,
  ShieldAlert
} from "lucide-react";
import { cn } from "@/lib/utils";

const sidebarItems = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Analytics", href: "/analytics", icon: BarChart3 },
  { label: "History", href: "/history", icon: History },
  { label: "Emergency", href: "/emergency", icon: ShieldAlert },
  { label: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden lg:flex flex-col w-64 min-h-screen border-r border-white/5 bg-slate-950/80 backdrop-blur-xl pt-20 pb-6 px-3">
      {/* Brand */}
      <div className="flex items-center gap-2.5 px-3 mb-8">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 shadow-lg shadow-cyan-500/30">
          <Activity className="h-4 w-4 text-white" />
        </div>
        <div>
          <p className="text-xs text-slate-500 font-medium uppercase tracking-widest">FlowSync</p>
          <p className="text-xs text-slate-600">City AI Platform v2.0</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1">
        {sidebarItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link key={item.href} href={item.href}>
              <motion.div
                whileHover={{ x: 4 }}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all cursor-pointer group relative",
                  isActive
                    ? "bg-gradient-to-r from-cyan-500/20 to-blue-500/10 text-cyan-300 border border-cyan-500/20"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="sidebar-active"
                    className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-cyan-400 rounded-full"
                  />
                )}
                <Icon className={cn("h-4 w-4", isActive ? "text-cyan-400" : "")} />
                {item.label}
                {isActive && (
                  <ChevronRight className="ml-auto h-3.5 w-3.5 text-cyan-400/60" />
                )}
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* Footer / Account */}
      <div className="mt-auto px-3 pt-4 border-t border-white/5 space-y-2">
        <Link href="/auth/login">
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-all cursor-pointer">
            <LogOut className="h-4 w-4" />
            <span>Sign Out</span>
          </div>
        </Link>
        <p className="text-[10px] text-slate-600 text-center">
          FlowSync Enterprise SaaS
        </p>
      </div>
    </aside>
  );
}
