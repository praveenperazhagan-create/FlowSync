"""
AI Service Bridge Layer
=======================

Integrates existing AI modules:
- ai.yolo.detect
- ai.inference.predict
- ai.inference.decision_engine
- ai.simulation.simulator
- ai.learning.logger

Executes the pipeline:
YOLO Detection -> Traffic Prediction -> Simulation -> Decision Engine -> Logger -> Return JSON
"""

import sys
import os
import time
from pathlib import Path
from PIL import Image
from io import BytesIO

from backend.app.config import AI_DIR
from backend.app.utils.tracker import logger

# Add AI Directory to sys.path automatically
if str(AI_DIR) not in sys.path:
    sys.path.insert(0, str(AI_DIR))

# Import AI core modules
try:
    from yolo.detect import detect_vehicles
    from inference.predict import predict_congestion, load_trained_model, load_encoders
    from inference.decision_engine import make_traffic_decision
    from simulation.simulator import simulate_signal_scenarios
    from learning.logger import log_prediction
except ImportError:
    from ai.yolo.detect import detect_vehicles
    from ai.inference.predict import predict_congestion, load_trained_model, load_encoders
    from ai.inference.decision_engine import make_traffic_decision
    from ai.simulation.simulator import simulate_signal_scenarios
    from ai.learning.logger import log_prediction


class AIService:
    _instance = None

    def __init__(self):
        self.model = None
        self.encoders = None
        self.is_loaded = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AIService()
        return cls._instance

    def load_ai_models(self):
        if self.is_loaded:
            return
        try:
            self.model = load_trained_model()
            self.encoders = load_encoders()
            self.is_loaded = True
            logger.info("Loaded AI models and encoders successfully.")
        except Exception as e:
            logger.warning(f"AI Model load warning: {e}")

    def execute_pipeline(
        self,
        image_bytes: bytes,
        city_zone: str = "Downtown",
        weather_condition: str = "Clear",
        visibility_km: float = 10.0,
        is_peak_hour: bool = False,
        incident_reported: bool = False,
        avg_speed_kmph: float = 40.0
    ) -> dict:
        if not image_bytes:
            raise ValueError("Image bytes are empty.")

        self.load_ai_models()

        # 1. Image -> PIL
        try:
            pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
        except Exception as exc:
            raise ValueError(f"Invalid image payload: {exc}") from exc

        # 2. YOLO Detection
        yolo_res = detect_vehicles(pil_image, return_json=False)

        cars = yolo_res.get("cars", yolo_res.get("counts", {}).get("car", 0))
        bikes = yolo_res.get("bikes", yolo_res.get("counts", {}).get("motorcycle", 0))
        bus = yolo_res.get("bus", yolo_res.get("counts", {}).get("bus", 0))
        truck = yolo_res.get("truck", yolo_res.get("counts", {}).get("truck", 0))
        emergency_vehicle_count = yolo_res.get("emergency_vehicle", 0)
        emergency_detected = yolo_res.get("emergency_vehicle_detected", False) or (emergency_vehicle_count > 0)
        total_vehicle_count = yolo_res.get("total_vehicle_count", yolo_res.get("total_vehicles", cars + bikes + bus + truck))

        # Heuristic speed adjustment if default
        if avg_speed_kmph == 40.0:
            if total_vehicle_count > 30:
                avg_speed_kmph = 12.0
            elif total_vehicle_count > 15:
                avg_speed_kmph = 25.0
            elif total_vehicle_count > 5:
                avg_speed_kmph = 45.0

        # 3. Traffic Prediction
        pred_res = predict_congestion(
            vehicle_count=total_vehicle_count,
            avg_speed_kmph=avg_speed_kmph,
            weather_condition=weather_condition,
            visibility_km=visibility_km,
            is_peak_hour=is_peak_hour,
            incident_reported=incident_reported,
            city_zone=city_zone,
            model=self.model,
            encoders=self.encoders
        )

        traffic_level = pred_res["predicted_congestion_level"]
        confidence = float(pred_res["confidence_pct"])

        # 4. Simulation
        sim_scenarios = simulate_signal_scenarios(
            vehicle_count=total_vehicle_count,
            avg_speed_kmph=avg_speed_kmph,
            weather_condition=weather_condition,
            visibility_km=visibility_km,
            incident_reported=incident_reported,
            signal_timings=[40, 60, 80, 100]
        )

        # 5. Decision Engine
        decision_res = make_traffic_decision(
            congestion_level=traffic_level,
            vehicle_count=total_vehicle_count,
            car_count=cars,
            bike_count=bikes,
            bus_count=bus,
            truck_count=truck,
            emergency_vehicle_count=emergency_vehicle_count,
            avg_speed_kmph=avg_speed_kmph,
            emergency_vehicle_detected=emergency_detected,
            visibility_km=visibility_km,
            weather_condition=weather_condition,
            city_zone=city_zone,
            is_peak_hour=is_peak_hour,
            incident_reported=incident_reported,
            simulation_scenarios=sim_scenarios
        )

        estimated_queue = decision_res.get("estimated_queue_length", max(5, int(total_vehicle_count * 0.5)))
        recommended_signal_time = decision_res["recommended_signal_time"]
        reasons = decision_res["reason_list"]

        # 6. Logger
        try:
            log_prediction(
                city_zone=city_zone,
                vehicle_count=total_vehicle_count,
                cars=cars,
                bikes=bikes,
                bus=bus,
                truck=truck,
                weather=weather_condition,
                visibility=visibility_km,
                prediction=traffic_level,
                confidence=confidence,
                recommended_signal_time=recommended_signal_time,
                queue_length=estimated_queue,
                waiting_time=float(sim_scenarios[0].get("waiting_time", 20.0) if sim_scenarios else 20.0)
            )
        except Exception as e:
            logger.warning(f"Logger append warning: {e}")

        # Exact output response mapping requested
        return {
            "traffic_level": traffic_level,
            "confidence": confidence,
            "recommended_signal_time": recommended_signal_time,
            "cars": cars,
            "bikes": bikes,
            "bus": bus,
            "truck": truck,
            "emergency_vehicle": emergency_detected,
            "estimated_queue": estimated_queue,
            "visibility": visibility_km,
            "reason": reasons,
            "summary": decision_res.get("summary", ""),
            "simulation_scenarios": sim_scenarios
        }


ai_service_bridge = AIService.get_instance()
