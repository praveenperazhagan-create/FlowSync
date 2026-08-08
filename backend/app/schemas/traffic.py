"""
Pydantic Schemas for FlowSync FastAPI Endpoints
================================================
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., example="running")


class AnalysisResponse(BaseModel):
    traffic_level: str = Field(..., example="High")
    confidence: float = Field(..., example=94.8)
    recommended_signal_time: int = Field(..., example=80)
    cars: int = Field(..., example=35)
    bikes: int = Field(..., example=14)
    bus: int = Field(..., example=3)
    truck: int = Field(..., example=2)
    emergency_vehicle: bool = Field(..., example=False)
    estimated_queue: int = Field(..., example=58)
    visibility: float = Field(..., example=8.2)
    reason: List[str] = Field(..., example=["Vehicle Count = 156", "Average Speed = 18 km/h", "Rain", "Peak Hour"])
    summary: Optional[str] = None
    simulation_scenarios: Optional[List[Dict[str, Any]]] = None


class VideoAnalysisResponse(BaseModel):
    filename: str
    total_frames_processed: int
    average_vehicle_counts: Dict[str, float]
    peak_congestion: str
    recommended_signal: int
    analysis_summary: Dict[str, Any]


class RetrainResponse(BaseModel):
    status: str = "success"
    accuracy: float
    training_time: str
    model_updated: bool
    details: Dict[str, Any]


class StatsResponse(BaseModel):
    current_model_accuracy: float
    images_processed: int
    videos_processed: int
    average_response_time_ms: float
    vehicle_detection_count: int
