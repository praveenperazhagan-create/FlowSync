"use client";
import { useState, useCallback } from "react";
import { analyzeTraffic } from "@/services/api";
import { TrafficAnalysisRequest, TrafficAnalysisResponse, AnalysisHistoryEntry } from "@/types/traffic";

export function useTrafficAnalysis() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<TrafficAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<AnalysisHistoryEntry[]>([]);

  const analyze = useCallback(async (params: TrafficAnalysisRequest) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await analyzeTraffic(params);
      setResult(data);

      const entry: AnalysisHistoryEntry = {
        id: Date.now().toString(),
        timestamp: new Date().toISOString(),
        traffic_level: data.traffic_level,
        confidence: data.confidence,
        vehicle_count: (data.cars + data.bikes + data.bus + data.truck),
        recommended_signal_time: data.recommended_signal_time,
        emergency_priority: data.emergency_priority || (data.emergency_vehicle ? "CRITICAL" : "LOW"),
        result: data,
      };
      setHistory((prev) => [entry, ...prev.slice(0, 9)]);
      return data;
    } catch (err: unknown) {
      const message =
        err instanceof Error
          ? err.message
          : "Failed to connect to the backend. Make sure the server is running.";
      setError(message);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearResult = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return { analyze, isLoading, result, error, history, clearResult };
}
