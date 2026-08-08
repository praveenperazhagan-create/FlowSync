"""
FlowSync AI Service Layer
=========================

Preloads YOLOv8 object detection model and Random Forest congestion classifier ONCE at startup.
Executes end-to-end traffic detection, prediction, simulation, decision reasoning, logging, and image annotation.
"""

import sys
import uuid
import cv2
import joblib
import numpy as np
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

from backend.config.config import AI_DIR, TRAFFIC_MODEL_PATH, YOLO_MODEL_PATH, OUTPUT_DIR
from backend.utils.logger import logger

# Add AI directory to sys.path for internal imports
if str(AI_DIR) not in sys.path:
    sys.path.insert(0, str(AI_DIR))

from inference.predict import predict_congestion, load_encoders
from inference.decision_engine import make_traffic_decision
from simulation.simulator import simulate_signal_scenarios
from learning.logger import log_prediction


class AIService:
    """
    Singleton AI Service class for model preloading and inference.
    """
    _instance = None

    def __init__(self):
        self.yolo_model = None
        self.traffic_model = None
        self.encoders = None
        self.is_loaded = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AIService()
        return cls._instance

    def load_models(self):
        """
        Loads YOLOv8, trained traffic model (.pkl), and encoders ONCE at server startup.
        """
        if self.is_loaded:
            logger.info("AI Models are already loaded in memory.")
            return

        logger.info("Initializing and preloading AI models at server startup...")

        # 1. Load YOLOv8 Model
        try:
            weights_path = YOLO_MODEL_PATH if YOLO_MODEL_PATH.exists() else "yolov8n.pt"
            logger.info(f"Loading YOLOv8 model from: {weights_path}")
            self.yolo_model = YOLO(str(weights_path))
            logger.info("YOLOv8 Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load YOLOv8 model: {e}")
            raise e

        # 2. Load Traffic Model (.pkl)
        try:
            logger.info(f"Loading Traffic Congestion model from: {TRAFFIC_MODEL_PATH}")
            if not TRAFFIC_MODEL_PATH.exists():
                raise FileNotFoundError(f"Model file not found at {TRAFFIC_MODEL_PATH}")
            self.traffic_model = joblib.load(TRAFFIC_MODEL_PATH)
            logger.info("Traffic Congestion ML Model (.pkl) loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Traffic Congestion model: {e}")
            raise e

        # 3. Load Encoders
        try:
            self.encoders = load_encoders()
            logger.info("Label Encoders loaded successfully.")
        except Exception as e:
            logger.warning(f"Label Encoders load warning: {e}")

        self.is_loaded = True
        logger.info("All AI Models successfully loaded into memory.")

    def process_traffic_analysis(
        self,
        image_path: Path,
        weather_condition: str = "Clear",
        visibility_km: float = 10.0,
        avg_speed_kmph: float = 40.0,
        city_zone: str = "Downtown",
        is_peak_hour: bool = False,
        incident_reported: bool = False
    ) -> dict:
        """
        Processes image through YOLO -> Prediction -> Simulation -> Decision Engine -> Logger.
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Input image file not found: {image_path}")

        if not self.is_loaded:
            self.load_models()

        logger.info(f"Starting analysis for image: {image_path.name}")

        # 1. Run YOLO Object Detection using preloaded model
        try:
            results = self.yolo_model(str(image_path), conf=0.25, verbose=False)
            result = results[0]
        except Exception as e:
            logger.error(f"YOLO inference failed for {image_path}: {e}")
            raise RuntimeError(f"YOLO inference failed: {e}") from e

        counts = {
            "car": 0,
            "motorcycle": 0,
            "bus": 0,
            "truck": 0,
            "ambulance": 0,
            "fire truck": 0,
            "police vehicle": 0
        }
        emergency_detected = False

        COCO_MAP = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

        for box in result.boxes:
            cls_id = int(box.cls[0].item())
            cls_name = None
            if hasattr(self.yolo_model, 'names') and cls_id in self.yolo_model.names:
                name = self.yolo_model.names[cls_id].lower()
                if name == "motorbike":
                    cls_name = "motorcycle"
                elif name in counts:
                    cls_name = name

            if cls_name is None and cls_id in COCO_MAP:
                cls_name = COCO_MAP[cls_id]

            if cls_name in counts:
                counts[cls_name] += 1
                if cls_name in ["ambulance", "fire truck", "police vehicle"]:
                    emergency_detected = True

        cars = counts["car"]
        bikes = counts["motorcycle"]
        buses = counts["bus"]
        trucks = counts["truck"]
        emergency_count = counts["ambulance"] + counts["fire truck"] + counts["police vehicle"]

        total_vehicles = cars + bikes + buses + trucks

        logger.info(f"YOLO Detection Summary: Total={total_vehicles} (Cars={cars}, Bikes={bikes}, Buses={buses}, Trucks={trucks})")

        # 2. Save Annotated Image
        annotated_filename = f"annotated_{image_path.name}"
        annotated_file_path = OUTPUT_DIR / annotated_filename

        try:
            annotated_frame = result.plot()
            cv2.imwrite(str(annotated_file_path), annotated_frame)
            logger.info(f"Saved annotated image to: {annotated_file_path}")
        except Exception as e:
            logger.warning(f"Failed to generate annotated image plot: {e}")
            annotated_filename = image_path.name

        # 3. Run ML Congestion Prediction
        prediction = predict_congestion(
            vehicle_count=total_vehicles,
            avg_speed_kmph=avg_speed_kmph,
            weather_condition=weather_condition,
            visibility_km=visibility_km,
            is_peak_hour=is_peak_hour,
            incident_reported=incident_reported,
            city_zone=city_zone,
            model=self.traffic_model,
            encoders=self.encoders
        )

        traffic_level = prediction["predicted_congestion_level"]
        confidence = float(prediction["confidence_pct"])

        logger.info(f"Congestion Prediction: Level='{traffic_level}', Confidence={confidence}%")

        # 4. Run Signal Simulation AI
        sim_scenarios = simulate_signal_scenarios(
            vehicle_count=total_vehicles,
            avg_speed_kmph=avg_speed_kmph,
            weather_condition=weather_condition,
            visibility_km=visibility_km,
            incident_reported=incident_reported,
            signal_timings=[40, 60, 80, 100]
        )

        # 5. Run AI Decision Engine
        decision = make_traffic_decision(
            congestion_level=traffic_level,
            vehicle_count=total_vehicles,
            car_count=cars,
            bike_count=bikes,
            bus_count=buses,
            truck_count=trucks,
            emergency_vehicle_count=emergency_count,
            avg_speed_kmph=avg_speed_kmph,
            emergency_vehicle_detected=emergency_detected,
            visibility_km=visibility_km,
            weather_condition=weather_condition,
            city_zone=city_zone,
            is_peak_hour=is_peak_hour,
            incident_reported=incident_reported,
            simulation_scenarios=sim_scenarios
        )

        # 6. Automatic Prediction Logging (Phase 5)
        try:
            log_prediction(
                city_zone=city_zone,
                vehicle_count=total_vehicles,
                cars=cars,
                bikes=bikes,
                bus=buses,
                truck=trucks,
                weather=weather_condition,
                visibility=visibility_km,
                prediction=traffic_level,
                confidence=confidence,
                recommended_signal_time=decision["recommended_signal_time"],
                queue_length=decision.get("estimated_queue_length", max(0, int(total_vehicles * 0.65))),
                waiting_time=float(decision.get("simulation_scenarios", [{}])[0].get("waiting_time", 20.0))
            )
        except Exception as e:
            logger.warning(f"Auto-logging prediction entry failed: {e}")

        # 7. Format Expected JSON Response
        response = {
            "traffic_level": traffic_level,
            "confidence": confidence,
            "vehicle_count": total_vehicles,
            "cars": cars,
            "bikes": bikes,
            "buses": buses,
            "trucks": trucks,
            "emergency_vehicle": emergency_count,
            "recommended_signal_time": decision["recommended_signal_time"],
            "current_signal_time": decision.get("current_signal_time", 60),
            "signal_difference": decision.get("signal_difference", decision["recommended_signal_time"] - 60),
            "estimated_queue_length": decision.get("estimated_queue_length", max(0, int(total_vehicles * 0.65))),
            "expected_congestion_reduction": decision["expected_congestion_reduction"],
            "expected_waiting_time_reduction": decision["expected_waiting_time_reduction"],
            "emergency_priority": decision["emergency_priority"],
            "reason_list": decision["reason_list"],
            "summary": decision.get("summary", ""),
            "simulation_scenarios": decision.get("simulation_scenarios", []),
            "annotated_image": f"output/{annotated_filename}"
        }

        return response


# Global AI Service instance
ai_service = AIService.get_instance()
