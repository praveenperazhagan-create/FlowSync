// FlowSync — Extended TypeScript Types

export type TrafficLevel = "Low" | "Moderate" | "High" | "Severe" | "Critical";
export type EmergencyPriority = "LOW" | "MODERATE" | "HIGH" | "CRITICAL";

export interface TrafficAnalysisRequest {
  image: File;
  weather_condition: string;
  visibility_km: number;
  avg_speed_kmph?: number;
  city_zone: string;
  is_peak_hour: boolean;
  incident_reported: boolean;
}

export interface SimulationScenario {
  signal_time: number;
  queue: number;
  waiting_time: number;
  average_speed: number;
  traffic_reduction: number;
  traffic_score: number;
}

export interface TrafficAnalysisResponse {
  traffic_level: TrafficLevel;
  confidence: number;
  recommended_signal_time: number;
  current_signal_time?: number;
  signal_difference?: number;
  cars: number;
  bikes: number;
  bus: number;
  buses?: number;
  truck: number;
  trucks?: number;
  emergency_vehicle: boolean;
  estimated_queue: number;
  estimated_queue_length?: number;
  expected_congestion_reduction?: string;
  expected_waiting_time_reduction?: string;
  emergency_priority?: EmergencyPriority;
  visibility: number;
  reason: string[];
  reason_list?: string[];
  summary?: string;
  simulation_scenarios?: SimulationScenario[];
  annotated_image?: string;
}

export interface VideoAnalysisResponse {
  filename: string;
  total_frames_processed: number;
  average_vehicle_counts: {
    cars: number;
    bikes: number;
    bus: number;
    truck: number;
  };
  peak_congestion: TrafficLevel;
  recommended_signal: number;
  analysis_summary: TrafficAnalysisResponse;
}

export interface HistoryRecord {
  timestamp: string;
  city_zone: string;
  vehicle_count: number;
  cars: number;
  bikes: number;
  bus: number;
  truck: number;
  weather: string;
  visibility: number;
  prediction: string;
  confidence: number;
  recommended_signal_time: number;
  queue_length: number;
  waiting_time: number;
}

export interface AnalysisHistoryEntry {
  id: string;
  timestamp: string;
  traffic_level: TrafficLevel;
  confidence: number;
  vehicle_count: number;
  recommended_signal_time: number;
  emergency_priority: EmergencyPriority;
  result: TrafficAnalysisResponse;
}

export interface RetrainResponse {
  status: string;
  accuracy: number;
  training_time: string;
  model_updated: boolean;
  details?: Record<string, any>;
}

export interface SystemStatsResponse {
  current_model_accuracy: number;
  images_processed: number;
  videos_processed: number;
  average_response_time_ms: number;
  vehicle_detection_count: number;
}

export interface UserProfile {
  name: string;
  email: string;
  role: string;
  zone: string;
  theme: "dark" | "light" | "system";
  notifications: boolean;
}
