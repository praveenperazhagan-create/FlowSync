"""
FlowSync Backend Configuration Module
=====================================
"""

import os
from pathlib import Path

# Resolve absolute paths automatically
BASE_DIR = Path(__file__).resolve().parent

# Check for the real AI folder under backend/ai first, then fall back to nearby locations.
POSSIBLE_AI_DIRS = [
    BASE_DIR.parent / "ai",
    BASE_DIR / "ai",
    BASE_DIR.parent.parent / "ai",
]

AI_DIR = None
for p in POSSIBLE_AI_DIRS:
    if p.exists() and p.is_dir():
        AI_DIR = p
        break

if AI_DIR is None:
    AI_DIR = BASE_DIR.parent / "ai"

# Directory configs
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# AI Artifact Paths
TRAFFIC_MODEL_PATH = AI_DIR / "models" / "traffic_model.pkl"
ENCODERS_PATH = AI_DIR / "models" / "encoders.pkl"
YOLO_MODEL_PATH = AI_DIR / "yolov8n.pt"
if not YOLO_MODEL_PATH.exists():
    YOLO_MODEL_PATH = AI_DIR / "yolo" / "yolov8n.pt"
if not YOLO_MODEL_PATH.exists():
    YOLO_MODEL_PATH = BASE_DIR.parent / "yolov8n.pt"
LOGS_DIR = AI_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
TRAFFIC_HISTORY_CSV = LOGS_DIR / "traffic_history.csv"

PROJECT_NAME = "FlowSync"
VERSION = "2.0.0"
HOST = "0.0.0.0"
PORT = 8000
