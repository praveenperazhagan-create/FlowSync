"""
FlowSync Traffic Analysis Routes
=================================

Defines all traffic-related API endpoints:
  POST /predict          — Full image analysis pipeline (YOLO + ML + Decision)
  POST /analyze/video    — Video frame extraction + full pipeline
  GET  /history          — Fetch prediction history as JSON records
  GET  /stats            — System stats (total predictions, model info)
  POST /retrain          — Trigger model retraining on logged data
"""

import os
import sys
import csv
import uuid
import shutil
import tempfile
from pathlib import Path
from typing import Optional

import cv2
from fastapi import APIRouter, File, Form, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from backend.config.config import UPLOADS_DIR, AI_DIR
from backend.services.ai_service import ai_service
from backend.utils.logger import logger

router = APIRouter()

# History log path (same as learning/logger.py resolves it)
LOGS_DIR = AI_DIR / "logs"
HISTORY_LOG_PATH = LOGS_DIR / "traffic_history.csv"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# POST /predict — Full Image Analysis Pipeline
# ---------------------------------------------------------------------------
@router.post(
    "/predict",
    summary="Analyze traffic image",
    description="Accepts an uploaded image with road conditions. Returns YOLO-detected vehicle counts, congestion prediction, and AI signal timing decision.",
    status_code=status.HTTP_200_OK
)
async def predict_traffic(
    image: UploadFile = File(..., description="Traffic camera image (jpg/png/webp)"),
    weather_condition: str = Form("Clear", description="Current weather condition (Clear, Rain, Fog, etc.)"),
    visibility_km: float = Form(10.0, description="Visibility in kilometers"),
    avg_speed_kmph: float = Form(40.0, description="Average vehicle speed in km/h"),
    city_zone: str = Form("Downtown", description="Zone of city (Downtown, Suburb, Commercial, etc.)"),
    is_peak_hour: bool = Form(False, description="Is this during peak traffic hours?"),
    incident_reported: bool = Form(False, description="Is a traffic incident reported?")
):
    """
    Full traffic analysis pipeline:
    1. Save uploaded image to backend/ai/uploads/
    2. Run YOLOv8 vehicle detection
    3. Run ML congestion prediction
    4. Run AI decision engine
    5. Return comprehensive JSON response
    """
    if not image.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file name was provided.")

    # Validate file type
    allowed_types = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
    content_type = image.content_type or ""
    if content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{content_type}'. Accepted: JPEG, PNG, WebP."
        )

    # Save uploaded image with a unique filename to avoid collisions
    unique_id = uuid.uuid4().hex[:8]
    safe_filename = f"{unique_id}_{image.filename.replace(' ', '_')}"
    upload_path = UPLOADS_DIR / safe_filename

    try:
        contents = await image.read()
        if not contents:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded image file is empty.")
        with open(upload_path, "wb") as f:
            f.write(contents)
        logger.info(f"Saved uploaded image to: {upload_path}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save uploaded image: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save uploaded image: {str(e)}"
        )

    # Run AI pipeline
    try:
        result = ai_service.process_traffic_analysis(
            image_path=upload_path,
            weather_condition=weather_condition,
            visibility_km=float(visibility_km),
            avg_speed_kmph=float(avg_speed_kmph),
            city_zone=city_zone,
            is_peak_hour=bool(is_peak_hour),
            incident_reported=bool(incident_reported)
        )
        logger.info(
            f"Analysis complete: traffic_level='{result['traffic_level']}', "
            f"vehicles={result['vehicle_count']}, signal={result['recommended_signal_time']}s"
        )
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)

    except FileNotFoundError as e:
        logger.error(f"Model file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI model not available: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Traffic analysis pipeline failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


# ---------------------------------------------------------------------------
# POST /analyze/video — Video Frame Extraction + Full Pipeline
# ---------------------------------------------------------------------------
@router.post(
    "/analyze/video",
    summary="Analyze traffic video",
    description="Extracts a representative keyframe from an uploaded video, then runs the full YOLO + ML + Decision pipeline.",
    status_code=status.HTTP_200_OK
)
async def analyze_video(
    file: UploadFile = File(..., description="Traffic video file (mp4/avi/mov)"),
    weather_condition: str = Form("Clear"),
    visibility_km: float = Form(10.0),
    avg_speed_kmph: float = Form(40.0),
    city_zone: str = Form("Downtown"),
    is_peak_hour: bool = Form(False),
    incident_reported: bool = Form(False)
):
    """
    Accepts a video file, extracts a representative keyframe,
    and runs the full traffic analysis pipeline on it.
    """
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    try:
        content = await file.read()
        temp_video.write(content)
        temp_video.close()

        cap = cv2.VideoCapture(temp_video.name)
        if not cap.isOpened():
            raise HTTPException(status_code=400, detail="Could not open video file.")

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_number = max(0, min(10, total_frames - 1))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            raise HTTPException(status_code=400, detail="Failed to extract frame from video.")

        # Save extracted frame as a temp image
        unique_id = uuid.uuid4().hex[:8]
        frame_filename = f"{unique_id}_video_frame.jpg"
        frame_path = UPLOADS_DIR / frame_filename
        cv2.imwrite(str(frame_path), frame)

        result = ai_service.process_traffic_analysis(
            image_path=frame_path,
            weather_condition=weather_condition,
            visibility_km=float(visibility_km),
            avg_speed_kmph=float(avg_speed_kmph),
            city_zone=city_zone,
            is_peak_hour=bool(is_peak_hour),
            incident_reported=bool(incident_reported)
        )

        result["video_metadata"] = {
            "filename": file.filename,
            "processed_frame_index": frame_number,
            "total_video_frames": total_frames
        }
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Video analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Video analysis failed: {str(e)}")
    finally:
        if os.path.exists(temp_video.name):
            os.remove(temp_video.name)


# ---------------------------------------------------------------------------
# GET /history — Fetch Prediction History as JSON
# ---------------------------------------------------------------------------
@router.get(
    "/history",
    summary="Get prediction history",
    description="Returns all logged traffic prediction records as a JSON array.",
    status_code=status.HTTP_200_OK
)
async def get_history():
    """
    Reads the traffic_history.csv log file and returns records as JSON.
    """
    if not HISTORY_LOG_PATH.exists() or HISTORY_LOG_PATH.stat().st_size == 0:
        return JSONResponse(content=[], status_code=status.HTTP_200_OK)

    try:
        records = []
        with open(HISTORY_LOG_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append({
                    "timestamp": row.get("timestamp", ""),
                    "city_zone": row.get("city_zone", ""),
                    "vehicle_count": int(row.get("vehicle_count", 0) or 0),
                    "cars": int(row.get("cars", 0) or 0),
                    "bikes": int(row.get("bikes", 0) or 0),
                    "bus": int(row.get("bus", 0) or 0),
                    "truck": int(row.get("truck", 0) or 0),
                    "weather": row.get("weather", ""),
                    "visibility": float(row.get("visibility", 10.0) or 10.0),
                    "prediction": row.get("prediction", ""),
                    "confidence": float(row.get("confidence", 0.0) or 0.0),
                    "recommended_signal_time": int(row.get("recommended_signal_time", 60) or 60),
                    "queue_length": int(row.get("queue_length", 0) or 0),
                    "waiting_time": float(row.get("waiting_time", 0.0) or 0.0),
                })
        logger.info(f"Fetched {len(records)} history records.")
        return JSONResponse(content=records, status_code=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Failed to read history log: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read history: {str(e)}"
        )


# ---------------------------------------------------------------------------
# GET /stats — System Statistics
# ---------------------------------------------------------------------------
@router.get(
    "/stats",
    summary="System statistics",
    description="Returns aggregate statistics about the FlowSync system.",
    status_code=status.HTTP_200_OK
)
async def get_stats():
    """
    Returns system-level statistics: total predictions, model status, etc.
    """
    total_predictions = 0
    congestion_counts = {"Low": 0, "Moderate": 0, "High": 0, "Severe": 0}
    total_vehicles = 0

    if HISTORY_LOG_PATH.exists() and HISTORY_LOG_PATH.stat().st_size > 0:
        try:
            with open(HISTORY_LOG_PATH, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_predictions += 1
                    pred = row.get("prediction", "").strip()
                    if pred in congestion_counts:
                        congestion_counts[pred] += 1
                    total_vehicles += int(row.get("vehicle_count", 0) or 0)
        except Exception as e:
            logger.warning(f"Could not compute stats from history: {e}")

    from backend.config.config import TRAFFIC_MODEL_PATH, YOLO_MODEL_PATH
    stats = {
        "current_model_accuracy": 0.0,
        "images_processed": total_predictions,
        "videos_processed": 0,
        "average_response_time_ms": 0.0,
        "vehicle_detection_count": total_vehicles,
        "total_predictions": total_predictions,
        "average_vehicles_per_analysis": round(total_vehicles / total_predictions, 1) if total_predictions > 0 else 0,
        "congestion_distribution": congestion_counts,
        "model_status": {
            "yolo_loaded": ai_service.is_loaded,
            "ml_model_loaded": ai_service.is_loaded,
            "yolo_model_path": str(YOLO_MODEL_PATH),
            "ml_model_path": str(TRAFFIC_MODEL_PATH),
        },
        "system": {
            "project": "FlowSync",
            "version": "1.0",
            "backend": "FastAPI + Uvicorn",
            "ml_stack": "YOLOv8 + Random Forest",
        }
    }
    return JSONResponse(content=stats, status_code=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# POST /retrain — Trigger Model Retraining
# ---------------------------------------------------------------------------
@router.post(
    "/retrain",
    summary="Retrain ML model",
    description="Merges prediction history logs with the base dataset and retrains the traffic congestion model.",
    status_code=status.HTTP_200_OK
)
async def retrain_model():
    """
    Triggers model retraining using logged prediction data.
    """
    try:
        # Add AI paths for retrain imports
        if str(AI_DIR) not in sys.path:
            sys.path.insert(0, str(AI_DIR))

        from learning.retrain import retrain_model as _retrain
        success = _retrain()

        if success:
            # Reload the updated model into the AI service singleton
            ai_service.is_loaded = False
            ai_service.load_models()
            logger.info("Model retraining complete. New model loaded into memory.")
            return JSONResponse(
                content={
                    "success": True,
                    "message": "Model retrained and reloaded successfully.",
                    "status": "complete"
                },
                status_code=status.HTTP_200_OK
            )
        else:
            raise Exception("Retraining returned False")

    except Exception as e:
        logger.error(f"Retraining failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Retraining failed: {str(e)}"
        )
