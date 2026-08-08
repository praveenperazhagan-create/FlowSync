
"""
YOLOv8 Vehicle Detection Engine
===============================

This script utilizes YOLOv8 to detect vehicles in traffic images or frame streams.
Detected target classes:
- car
- motorcycle
- bus
- truck
- ambulance
- fire truck
- police vehicle

Outputs a JSON payload containing vehicle counts, emergency vehicle detection status,
and detailed object bounding boxes.
"""

import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from inference.predict import predict_congestion
import json
import numpy as np
from PIL import Image, ImageDraw

from inference.decision_engine import make_traffic_decision
# Target vehicle classes requested
TARGET_VEHICLE_CLASSES = [
    "car",
    "motorcycle",
    "bus",
    "truck",
    "ambulance",
    "fire truck",
    "police vehicle"
]

# Standard COCO dataset class index mapping for YOLOv8
COCO_CLASS_MAP = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

EMERGENCY_CLASSES = ["ambulance", "fire truck", "police vehicle"]


def get_yolo_model(model_weights: str = "yolov8n.pt"):
    """
    Lazy loader for YOLOv8 model.
    """
    try:
        from ultralytics import YOLO
        print(f"[INFO] Loading YOLOv8 model with weights: {model_weights}")
        model = YOLO(model_weights)
        return model
    except ImportError as e:
        raise ImportError(
            "Ultralytics package not found. Please install it using `pip install ultralytics`."
        ) from e


def detect_vehicles(
    image_source,
    model_weights: str = "yolov8n.pt",
    conf_threshold: float = 0.25,
    return_json: bool = True
):
    """
    Runs YOLOv8 object detection on an image and counts target vehicle categories.

    Parameters:
        image_source (str or PIL.Image or np.ndarray): Image file path, PIL Image, or numpy array.
        model_weights (str): Path to YOLO weights file (e.g. 'yolov8n.pt' or custom trained model).
        conf_threshold (float): Minimum confidence threshold for detection (0.0 to 1.0).
        return_json (bool): If True, returns formatted JSON string; else returns dictionary.

    Returns:
        str or dict: Detection summary containing vehicle counts and emergency vehicle status.
    """
    # Load model
    model = get_yolo_model(model_weights)

    # Initialize count dictionary
    counts = {category: 0 for category in TARGET_VEHICLE_CLASSES}
    detected_objects = []
    emergency_detected = False

    # Run inference
    results = model(image_source, conf=conf_threshold, verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            xyxy = box.xyxy[0].tolist()  # [xmin, ymin, xmax, ymax]

            # Check if detected class is in standard model names or custom COCO mapping
            class_name = None
            if hasattr(model, 'names') and cls_id in model.names:
                model_cls_name = model.names[cls_id].lower()
                if model_cls_name in TARGET_VEHICLE_CLASSES:
                    class_name = model_cls_name
                elif model_cls_name == "motorbike":
                    class_name = "motorcycle"

            if class_name is None and cls_id in COCO_CLASS_MAP:
                class_name = COCO_CLASS_MAP[cls_id]

            # Register detection if it matches target categories
            if class_name in counts:
                counts[class_name] += 1
                if class_name in EMERGENCY_CLASSES:
                    emergency_detected = True

                detected_objects.append({
                    "class": class_name,
                    "confidence": round(conf, 4),
                    "bbox": [round(coord, 2) for coord in xyxy]
                })

    total_vehicles = sum(counts.values())
    emergency_vehicle_count = (
        counts.get("ambulance", 0) +
        counts.get("fire truck", 0) +
        counts.get("police vehicle", 0)
    )

    summary = {
        "cars": counts.get("car", 0),
        "bikes": counts.get("motorcycle", 0),
        "bus": counts.get("bus", 0),
        "truck": counts.get("truck", 0),
        "emergency_vehicle": emergency_vehicle_count,
        "total_vehicle_count": total_vehicles,
        "counts": counts,
        "emergency_vehicle_detected": emergency_detected,
        "total_vehicles": total_vehicles,
        "detected_objects": detected_objects
    }

    if return_json:
        return json.dumps(summary, indent=2)
    return summary


def create_sample_traffic_image(output_path: str = "sample_traffic.jpg") -> str:
    """
    Creates a synthetic traffic image for testing YOLOv8 detection.
    """
    img = Image.new("RGB", (640, 480), color=(100, 100, 100))
    draw = ImageDraw.Draw(img)

    # Draw road background
    draw.rectangle([0, 140, 640, 340], fill=(50, 50, 50))
    # Lane markers
    for x in range(0, 640, 40):
        draw.line([(x, 240), (x + 20, 240)], fill=(255, 255, 255), width=3)

    # Draw vehicle representations
    # Car 1
    draw.rectangle([50, 160, 150, 220], fill=(200, 30, 30))
    # Car 2
    draw.rectangle([200, 250, 310, 310], fill=(30, 30, 200))
    # Bus
    draw.rectangle([350, 150, 520, 230], fill=(220, 220, 30))
    # Motorcycle
    draw.rectangle([550, 260, 590, 300], fill=(30, 200, 30))

    img.save(output_path)
    print(f"[INFO] Synthetic traffic sample image saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    print("=" * 60)
    print(" FLOWSYNC YOLO VEHICLE DETECTION ")
    print("=" * 60)

    image_path = input("Enter image path: ").strip()

    if not os.path.exists(image_path):
        print("[ERROR] Image not found!")
        sys.exit()

    print(f"\n[INFO] Running detection on: {image_path}")

    result = detect_vehicles(image_path, return_json=False)

    vehicle_count = result["total_vehicle_count"]

    cars = result["cars"]
    bikes = result["bikes"]
    buses = result["bus"]
    trucks = result["truck"]

    prediction = predict_congestion(
        vehicle_count=vehicle_count,
        avg_speed_kmph=25.0,
        weather_condition="Clear",
        visibility_km=10.0,
        is_peak_hour=False,
        incident_reported=False,
        city_zone="Downtown"
    )
    decision = make_traffic_decision(
        congestion_level=prediction["predicted_congestion_level"],
        vehicle_count=vehicle_count,
        car_count=cars,
        bike_count=bikes,
        bus_count=buses,
        truck_count=trucks,
        emergency_vehicle_count=0,
        avg_speed_kmph=25.0,
        weather_condition="Clear",
        visibility_km=10.0,
        is_peak_hour=False,
        incident_reported=False
    )
    print("\n===== Vehicle Detection =====")

    print("Cars :", cars)
    print("Bikes :", bikes)
    print("Bus :", buses)
    print("Truck :", trucks)

    print("Total :", vehicle_count)
    print("\n===== AI Prediction =====")

    print(f"Traffic Level : {prediction['predicted_congestion_level']}")
    print(f"Confidence    : {prediction['confidence_pct']}%")

    print("\nClass Probabilities:")

    for level, prob in prediction["class_probabilities"].items():
        print(f"{level:<10}: {prob}%")
    print("\n===== FlowSync AI Decision =====")

    print(f"Recommended Signal Time : {decision['recommended_signal_time']} sec")

    print("\nReasons:")

    for reason in decision["reason_list"]:
        print("✓", reason)