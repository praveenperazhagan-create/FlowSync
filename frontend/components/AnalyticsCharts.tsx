"use client";
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, LineChart, Line, Legend,
} from "recharts";
import { TrafficAnalysisResponse, AnalysisHistoryEntry } from "@/types/traffic";
import { motion } from "framer-motion";

interface AnalyticsChartsProps {
  result: TrafficAnalysisResponse;
  history: AnalysisHistoryEntry[];
}

const PIE_COLORS = ["#06b6d4", "#a855f7", "#3b82f6", "#f97316"];

const tooltipStyle = {
  backgroundColor: "#0f172a",
  border: "1px solid rgba(255,255,255,0.08)",
  borderRadius: "8px",
  color: "#cbd5e1",
  fontSize: "12px",
};

export function AnalyticsCharts({ result, history }: AnalyticsChartsProps) {
  const vehicleData = [
    { name: "Cars", value: result.cars || 0 },
    { name: "Bikes", value: result.bikes || 0 },
    { name: "Buses", value: result.buses || result.bus || 0 },
    { name: "Trucks", value: result.trucks || result.truck || 0 },
  ].filter((d) => (d.value || 0) > 0);

  const signalData = [
    { label: "Current", value: result.current_signal_time, fill: "#475569" },
    { label: "Recommended", value: result.recommended_signal_time, fill: "#06b6d4" },
  ];

  const trendData = history
    .slice()
    .reverse()
    .map((entry, i) => ({
      time: `T-${history.length - i}`,
      vehicles: entry.vehicle_count,
      confidence: Math.round(entry.confidence),
      signal: entry.recommended_signal_time,
    }));

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Vehicle Distribution — Pie */}
        <ChartCard title="Vehicle Distribution">
          {vehicleData.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie
                  data={vehicleData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {vehicleData.map((_, index) => (
                    <Cell key={index} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={tooltipStyle} />
                <Legend
                  iconType="circle"
                  iconSize={8}
                  formatter={(v) => <span className="text-xs text-slate-400">{v}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex h-[220px] items-center justify-center text-slate-500 text-sm">
              No vehicles detected
            </div>
          )}
        </ChartCard>

        {/* Signal Timing — Bar */}
        <ChartCard title="Signal Timing Comparison">
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={signalData} barCategoryGap="40%">
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="label" tick={{ fill: "#64748b", fontSize: 11 }} axisLine={false} />
              <YAxis tick={{ fill: "#64748b", fontSize: 11 }} axisLine={false} tickLine={false} unit="s" />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {signalData.map((d, i) => (
                  <Cell key={i} fill={d.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Traffic Trend — Line */}
      {trendData.length >= 2 && (
        <ChartCard title="Traffic Trend (Analysis History)">
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="time" tick={{ fill: "#64748b", fontSize: 11 }} axisLine={false} />
              <YAxis tick={{ fill: "#64748b", fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Legend
                iconType="circle"
                iconSize={8}
                formatter={(v) => <span className="text-xs text-slate-400">{v}</span>}
              />
              <Line
                type="monotone"
                dataKey="vehicles"
                stroke="#06b6d4"
                strokeWidth={2}
                dot={{ r: 3, fill: "#06b6d4" }}
                name="Vehicles"
              />
              <Line
                type="monotone"
                dataKey="signal"
                stroke="#a855f7"
                strokeWidth={2}
                dot={{ r: 3, fill: "#a855f7" }}
                name="Signal (s)"
              />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>
      )}
    </div>
  );
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-xl border border-white/8 bg-slate-900/60 backdrop-blur-xl p-5"
    >
      <p className="text-sm font-semibold text-white mb-4">{title}</p>
      {children}
    </motion.div>
  );
}
