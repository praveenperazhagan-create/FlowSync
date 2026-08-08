import axios from "axios";
import {
  TrafficAnalysisRequest,
  TrafficAnalysisResponse,
  VideoAnalysisResponse,
  RetrainResponse,
  SystemStatsResponse,
  HistoryRecord
} from "@/types/traffic";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 60000,
});

export async function checkHealth(): Promise<{ status: string }> {
  const response = await apiClient.get<{ status: string }>("/health");
  return response.data;
}

export async function analyzeTraffic(
  params: TrafficAnalysisRequest
): Promise<TrafficAnalysisResponse> {
  const formData = new FormData();
  formData.append("image", params.image);
  formData.append("city_zone", params.city_zone);
  formData.append("weather_condition", params.weather_condition);
  formData.append("visibility_km", String(params.visibility_km));
  formData.append("avg_speed_kmph", String(params.avg_speed_kmph ?? 40.0)); // Fix 4: was missing
  formData.append("is_peak_hour", String(params.is_peak_hour));
  formData.append("incident_reported", String(params.incident_reported));

  // Fix 1: was "/analyze" — backend route is "/predict"
  const response = await apiClient.post<TrafficAnalysisResponse>(
    "/predict",
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );

  const data = response.data;
  // Normalize alias properties
  data.buses = data.buses ?? data.bus;
  data.trucks = data.trucks ?? data.truck;
  data.current_signal_time = data.current_signal_time ?? 60;
  data.signal_difference = data.signal_difference ?? (data.recommended_signal_time - 60);
  data.estimated_queue_length = data.estimated_queue_length ?? data.estimated_queue;
  data.expected_congestion_reduction = data.expected_congestion_reduction ?? "25%";
  data.expected_waiting_time_reduction = data.expected_waiting_time_reduction ?? "30%";
  data.emergency_priority = data.emergency_priority ?? (data.emergency_vehicle ? "CRITICAL" : "LOW");
  data.reason_list = data.reason_list ?? data.reason;

  return data;
}

export async function analyzeImage(
  params: TrafficAnalysisRequest
): Promise<TrafficAnalysisResponse> {
  return analyzeTraffic(params);
}

export async function analyzeVideo(
  videoFile: File,
  city_zone: string = "Downtown",
  weather_condition: string = "Clear",
  visibility_km: number = 10.0,
  is_peak_hour: boolean = false,
  incident_reported: boolean = false
): Promise<VideoAnalysisResponse> {
  const formData = new FormData();
  formData.append("file", videoFile);
  formData.append("city_zone", city_zone);
  formData.append("weather_condition", weather_condition);
  formData.append("visibility_km", String(visibility_km));
  formData.append("is_peak_hour", String(is_peak_hour));
  formData.append("incident_reported", String(incident_reported));

  // Fix 1: was "/video" — backend route is "/analyze/video"
  const response = await apiClient.post<VideoAnalysisResponse>(
    "/analyze/video",
    formData,
    {
      headers: { "Content-Type": "multipart/form-data" },
    }
  );
  return response.data;
}

export async function fetchHistory(): Promise<HistoryRecord[]> {
  const response = await apiClient.get<HistoryRecord[]>("/history");
  return response.data;
}

export async function triggerRetraining(): Promise<RetrainResponse> {
  const response = await apiClient.post<RetrainResponse>("/retrain");
  return response.data;
}

export async function fetchSystemStats(): Promise<SystemStatsResponse> {
  const response = await apiClient.get<SystemStatsResponse>("/stats");
  return response.data;
}
