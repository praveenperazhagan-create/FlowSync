"use client";
import { useCallback, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, ImageIcon, X, Cloud, Eye, Gauge, MapPin, Siren, AlertTriangle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { TrafficAnalysisRequest } from "@/types/traffic";
import { toast } from "sonner";

interface UploadCardProps {
  onAnalyze: (params: TrafficAnalysisRequest) => Promise<void>;
  isLoading: boolean;
}

const WEATHER_OPTIONS = ["Clear", "Rain", "Fog", "Cloudy", "Storm", "Snow"];
const CITY_ZONES = ["Downtown", "Suburb", "Commercial", "Industrial", "Highway", "Residential"];

export function UploadCard({ onAnalyze, isLoading }: UploadCardProps) {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Form state
  const [weather, setWeather] = useState("Clear");
  const [visibility, setVisibility] = useState(10);
  const [avgSpeed, setAvgSpeed] = useState(40);
  const [cityZone, setCityZone] = useState("Downtown");
  const [isPeakHour, setIsPeakHour] = useState(false);
  const [incidentReported, setIncidentReported] = useState(false);

  const handleFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      toast.error("Please upload a valid image file (JPG, PNG, WebP)");
      return;
    }
    setImage(file);
    const reader = new FileReader();
    reader.onloadend = () => setPreview(reader.result as string);
    reader.readAsDataURL(file);
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, []);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!image) {
      toast.error("Please upload a traffic image first");
      return;
    }
    await onAnalyze({
      image,
      weather_condition: weather,
      visibility_km: visibility,
      avg_speed_kmph: avgSpeed,
      city_zone: cityZone,
      is_peak_hour: isPeakHour,
      incident_reported: incidentReported,
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-white/10 bg-slate-900/60 backdrop-blur-xl shadow-2xl p-6"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/20">
          <Upload className="h-4 w-4 text-cyan-400" />
        </div>
        <div>
          <h2 className="text-base font-semibold text-white">Traffic Image Analysis</h2>
          <p className="text-xs text-slate-500">Upload a traffic camera image</p>
        </div>
      </div>

      <form onSubmit={onSubmit} className="space-y-5">
        {/* Drop Zone */}
        <div
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={onDrop}
          onClick={() => fileInputRef.current?.click()}
          className={cn(
            "relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed cursor-pointer transition-all min-h-[180px]",
            isDragging
              ? "border-cyan-400 bg-cyan-500/10"
              : preview
              ? "border-cyan-500/40 bg-slate-800/50"
              : "border-white/10 bg-slate-800/30 hover:border-cyan-500/40 hover:bg-slate-800/50"
          )}
        >
          <AnimatePresence mode="wait">
            {preview ? (
              <motion.div
                key="preview"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                className="relative w-full"
              >
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={preview}
                  alt="Traffic preview"
                  className="w-full max-h-44 object-cover rounded-lg"
                />
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    setImage(null);
                    setPreview(null);
                  }}
                  className="absolute top-2 right-2 flex h-7 w-7 items-center justify-center rounded-full bg-slate-900/80 border border-white/10 text-slate-300 hover:text-white transition-colors"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
                <div className="absolute bottom-2 left-2 rounded-md bg-slate-900/80 border border-white/10 px-2 py-1">
                  <p className="text-xs text-slate-300 truncate max-w-[140px]">{image?.name}</p>
                </div>
              </motion.div>
            ) : (
              <motion.div
                key="dropzone"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center gap-3 py-8 px-4"
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/20">
                  <ImageIcon className="h-6 w-6 text-cyan-400" />
                </div>
                <div className="text-center">
                  <p className="text-sm font-medium text-white">Drag & drop or click to upload</p>
                  <p className="text-xs text-slate-500 mt-1">JPG, PNG, WebP supported</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => { if (e.target.files?.[0]) handleFile(e.target.files[0]); }}
          />
        </div>

        {/* Form Fields */}
        <div className="grid grid-cols-2 gap-3">
          {/* Weather */}
          <div className="space-y-1.5">
            <label className="flex items-center gap-1.5 text-xs text-slate-400">
              <Cloud className="h-3.5 w-3.5 text-cyan-400" /> Weather
            </label>
            <select
              value={weather}
              onChange={(e) => setWeather(e.target.value)}
              className="w-full rounded-lg border border-white/10 bg-slate-800/60 px-3 py-2 text-sm text-white focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
            >
              {WEATHER_OPTIONS.map((w) => <option key={w} value={w}>{w}</option>)}
            </select>
          </div>

          {/* City Zone */}
          <div className="space-y-1.5">
            <label className="flex items-center gap-1.5 text-xs text-slate-400">
              <MapPin className="h-3.5 w-3.5 text-purple-400" /> City Zone
            </label>
            <select
              value={cityZone}
              onChange={(e) => setCityZone(e.target.value)}
              className="w-full rounded-lg border border-white/10 bg-slate-800/60 px-3 py-2 text-sm text-white focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
            >
              {CITY_ZONES.map((z) => <option key={z} value={z}>{z}</option>)}
            </select>
          </div>

          {/* Visibility */}
          <div className="space-y-1.5">
            <label className="flex items-center gap-1.5 text-xs text-slate-400">
              <Eye className="h-3.5 w-3.5 text-blue-400" /> Visibility (km)
            </label>
            <input
              type="number"
              min={0.1}
              max={50}
              step={0.1}
              value={visibility}
              onChange={(e) => setVisibility(Number(e.target.value))}
              className="w-full rounded-lg border border-white/10 bg-slate-800/60 px-3 py-2 text-sm text-white focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
            />
          </div>

          {/* Avg Speed */}
          <div className="space-y-1.5">
            <label className="flex items-center gap-1.5 text-xs text-slate-400">
              <Gauge className="h-3.5 w-3.5 text-yellow-400" /> Avg Speed (km/h)
            </label>
            <input
              type="number"
              min={0}
              max={200}
              value={avgSpeed}
              onChange={(e) => setAvgSpeed(Number(e.target.value))}
              className="w-full rounded-lg border border-white/10 bg-slate-800/60 px-3 py-2 text-sm text-white focus:border-cyan-500/50 focus:outline-none focus:ring-1 focus:ring-cyan-500/20"
            />
          </div>
        </div>

        {/* Toggles */}
        <div className="flex gap-4">
          <Toggle
            label="Peak Hour"
            checked={isPeakHour}
            onChange={setIsPeakHour}
            color="cyan"
          />
          <Toggle
            label="Incident Reported"
            checked={incidentReported}
            onChange={setIncidentReported}
            color="red"
            Icon={<Siren className="h-3.5 w-3.5" />}
          />
        </div>

        {/* Submit */}
        <motion.button
          type="submit"
          disabled={isLoading || !image}
          whileHover={{ scale: isLoading || !image ? 1 : 1.01 }}
          whileTap={{ scale: isLoading || !image ? 1 : 0.98 }}
          className={cn(
            "w-full flex items-center justify-center gap-2 rounded-xl py-3 text-sm font-semibold transition-all",
            isLoading || !image
              ? "bg-slate-800 text-slate-500 cursor-not-allowed"
              : "bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/20 hover:shadow-cyan-500/40"
          )}
        >
          {isLoading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Analyzing with AI...
            </>
          ) : (
            <>
              <AlertTriangle className="h-4 w-4" />
              Analyze Traffic
            </>
          )}
        </motion.button>
      </form>
    </motion.div>
  );
}

function Toggle({
  label,
  checked,
  onChange,
  color,
  Icon,
}: {
  label: string;
  checked: boolean;
  onChange: (v: boolean) => void;
  color: "cyan" | "red";
  Icon?: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      className={cn(
        "flex-1 flex items-center justify-between gap-2 rounded-lg border px-3 py-2.5 text-xs font-medium transition-all",
        checked
          ? color === "cyan"
            ? "border-cyan-500/40 bg-cyan-500/10 text-cyan-300"
            : "border-red-500/40 bg-red-500/10 text-red-300"
          : "border-white/10 bg-slate-800/50 text-slate-400 hover:border-white/20"
      )}
    >
      <span className="flex items-center gap-1.5">
        {Icon}
        {label}
      </span>
      <div
        className={cn(
          "relative h-4 w-7 rounded-full transition-colors",
          checked
            ? color === "cyan" ? "bg-cyan-500" : "bg-red-500"
            : "bg-slate-700"
        )}
      >
        <div
          className={cn(
            "absolute top-0.5 h-3 w-3 rounded-full bg-white shadow transition-transform",
            checked ? "translate-x-3" : "translate-x-0.5"
          )}
        />
      </div>
    </button>
  );
}
