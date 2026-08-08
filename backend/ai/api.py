"""
FlowSync AI Traffic Control REST API (FastAPI)
=============================================

This FastAPI application provides real-time intelligent traffic management APIs:
1. Upload Image / Video -> Runs YOLOv8 vehicle detection.
2. Runs ML Congestion Predictor (`predict_congestion`).
3. Runs Adaptive AI Decision Engine (`make_traffic_decision`).
4. Returns comprehensive JSON output with counts, predictions, signal timing, and reduction metrics.
"""

import os
import sys
import tempfile
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Ensure subdirectories are on sys.path for both package and direct imports
ai_dir = os.path.dirname(os.path.abspath(__file__))
for path in [ai_dir, os.path.join(ai_dir, "inference"), os.path.join(ai_dir, "training"), os.path.join(ai_dir, "yolo")]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from inference.predict import predict_congestion
    from inference.decision_engine import make_traffic_decision
    from yolo.detect import detect_vehicles
except (ImportError, ModuleNotFoundError):
    try:
        from predict import predict_congestion
        from decision_engine import make_traffic_decision
        from detect import detect_vehicles
    except (ImportError, ModuleNotFoundError):
        from ai.inference.predict import predict_congestion
        from ai.inference.decision_engine import make_traffic_decision
        from ai.yolo.detect import detect_vehicles

# Initialize FastAPI App
app = FastAPI(
    title="FlowSync AI Traffic Management API",
    description="Integrated API for YOLO Vehicle Detection, Congestion Prediction & AI Signal Decision Engine",
    version="1.0.0"
)

# Enable CORS for cross-origin frontend apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ManualInferenceRequest(BaseModel):
    vehicle_count: int = 150
    avg_speed_kmph: float = 35.0
    weather_condition: str = "Clear"
    visibility_km: float = 10.0
    is_peak_hour: bool = False
    incident_reported: bool = False
    emergency_vehicle_detected: bool = False
    city_zone: str = "Downtown"

@app.get("/health")
async def health():
    return {
        "status": "running",
        "message": "FlowSync Backend Online"
    }

@app.get("/")
def read_root():
    """
    Health check and root API endpoint.
    """
    return {
        "status": "online",
        "system": "FlowSync AI Traffic Control Engine",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze/image": "Upload image file for YOLO detection + Prediction + Decision Engine",
            "POST /analyze/video": "Upload video file for YOLO frame detection + Prediction + Decision Engine",
            "POST /analyze/manual": "Send JSON payload for manual inference & decision response"
        }
    }


def process_image_and_run_pipeline(
    image_bytes: bytes,
    weather_condition: str = "Clear",
    visibility_km: float = 10.0,
    city_zone: str = "Downtown",
    is_peak_hour: bool = False,
    incident_reported: bool = False,
    avg_speed_kmph: Optional[float] = None
) -> dict:
    """
    Core pipeline function: Image -> YOLO -> ML Prediction -> Decision Engine -> JSON
    """
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image file is empty.")

    # Load Image with PIL
    try:
        pil_image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file format: {e}") from e

    # 1. Run YOLO Detection
    yolo_result = detect_vehicles(pil_image, return_json=False)

    detected_counts = yolo_result["counts"]
    total_vehicles = yolo_result["total_vehicles"]
    emergency_detected = yolo_result["emergency_vehicle_detected"]

    # Estimate speed dynamically based on density if not supplied
    if avg_speed_kmph is None:
        # Heuristic speed estimation based on vehicle density
        if total_vehicles > 30:
            avg_speed_kmph = 12.0
        elif total_vehicles > 15:
            avg_speed_kmph = 25.0
        elif total_vehicles > 5:
            avg_speed_kmph = 45.0
        else:
            avg_speed_kmph = 60.0

    # 2. Run Congestion ML Prediction
    prediction_result = predict_congestion(
        vehicle_count=total_vehicles,
        avg_speed_kmph=avg_speed_kmph,
        weather_condition=weather_condition,
        visibility_km=visibility_km,
        is_peak_hour=is_peak_hour,
        incident_reported=incident_reported,
        city_zone=city_zone
    )

    predicted_congestion = prediction_result["predicted_congestion_level"]

    # 3. Run AI Decision Engine
    decision_result = make_traffic_decision(
        congestion_level=predicted_congestion,
        vehicle_count=total_vehicles,
        avg_speed_kmph=avg_speed_kmph,
        emergency_vehicle_detected=emergency_detected,
        visibility_km=visibility_km,
        weather_condition=weather_condition,
        city_zone=city_zone,
        is_peak_hour=is_peak_hour,
        incident_reported=incident_reported
    )

    # 4. Construct Integrated JSON Response
    response_data = {
        "success": True,
        "input_summary": {
            "weather_condition": weather_condition,
            "visibility_km": visibility_km,
            "city_zone": city_zone,
            "is_peak_hour": is_peak_hour,
            "incident_reported": incident_reported,
            "estimated_avg_speed_kmph": round(avg_speed_kmph, 1)
        },
        "yolo_detection": yolo_result,
        "congestion_prediction": prediction_result,
        "decision_engine": decision_result
    }

    return response_data


@app.post("/analyze/image")
async def analyze_image(
    file: UploadFile = File(...),
    weather_condition: str = Form("Clear"),
    visibility_km: float = Form(10.0),
    city_zone: str = Form("Downtown"),
    is_peak_hour: bool = Form(False),
    incident_reported: bool = Form(False),
    avg_speed_kmph: Optional[float] = Form(None)
):
    """
    Accepts an uploaded image file, runs YOLO detection, congestion prediction, and decision engine.
    """
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    return process_image_and_run_pipeline(
        image_bytes=contents,
        weather_condition=weather_condition,
        visibility_km=visibility_km,
        city_zone=city_zone,
        is_peak_hour=is_peak_hour,
        incident_reported=incident_reported,
        avg_speed_kmph=avg_speed_kmph
    )


@app.post("/analyze/video")
async def analyze_video(
    file: UploadFile = File(...),
    weather_condition: str = Form("Clear"),
    visibility_km: float = Form(10.0),
    city_zone: str = Form("Downtown"),
    is_peak_hour: bool = Form(False),
    incident_reported: bool = Form(False)
):
    """
    Accepts an uploaded video file, extracts representative keyframe, runs YOLO detection, prediction, and decision engine.
    """
    # Write uploaded video to temporary file
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    try:
        content = await file.read()
        temp_video.write(content)
        temp_video.close()

        # Capture keyframe using OpenCV
        cap = cv2.VideoCapture(temp_video.name)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Could not open video file.")

        # Read sample frame near start
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_number = max(0, min(10, total_frames - 1))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            raise HTTPException(status_code=400, detail="Failed to extract frame from uploaded video.")

        # Convert BGR frame to RGB image bytes
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        # Execute processing pipeline on extracted frame
        result = process_image_and_run_pipeline(
            image_bytes=frame_bytes,
            weather_condition=weather_condition,
            visibility_km=visibility_km,
            city_zone=city_zone,
            is_peak_hour=is_peak_hour,
            incident_reported=incident_reported
        )
        result["video_metadata"] = {
            "filename": file.filename,
            "processed_frame_index": frame_number,
            "total_video_frames": total_frames
        }
        return result

    finally:
        if os.path.exists(temp_video.name):
            os.remove(temp_video.name)


@app.post("/analyze/manual")
def analyze_manual(request: ManualInferenceRequest):
    """
    Accepts manual JSON request parameters and runs Congestion Prediction + AI Decision Engine.
    """
    pred_result = predict_congestion(
        vehicle_count=request.vehicle_count,
        avg_speed_kmph=request.avg_speed_kmph,
        weather_condition=request.weather_condition,
        visibility_km=request.visibility_km,
        is_peak_hour=request.is_peak_hour,
        incident_reported=request.incident_reported,
        city_zone=request.city_zone
    )

    decision_result = make_traffic_decision(
        congestion_level=pred_result["predicted_congestion_level"],
        vehicle_count=request.vehicle_count,
        avg_speed_kmph=request.avg_speed_kmph,
        emergency_vehicle_detected=request.emergency_vehicle_detected,
        visibility_km=request.visibility_km,
        weather_condition=request.weather_condition,
        city_zone=request.city_zone,
        is_peak_hour=request.is_peak_hour,
        incident_reported=request.incident_reported
    )

    return {
        "success": True,
        "manual_input": request.model_dump(),
        "congestion_prediction": pred_result,
        "decision_engine": decision_result
    }


if __name__ == "__main__":
    import uvicorn
    print("[INFO] Starting FlowSync FastAPI server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
