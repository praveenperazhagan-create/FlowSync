"""
FlowSync Backend Configuration Settings
========================================

Uses pathlib for robust, OS-independent path resolution across the project.
"""

import os
from pathlib import Path

# Base Directories using pathlib
BASE_DIR = Path(__file__).resolve().parent.parent  # backend/
PROJECT_ROOT = BASE_DIR.parent                      # FlowSync/

# AI Module Directories
AI_DIR = BASE_DIR / "ai"
MODELS_DIR = AI_DIR / "models"
TRAFFIC_MODEL_PATH = MODELS_DIR / "traffic_model.pkl"
YOLO_MODEL_PATH = AI_DIR / "yolov8n.pt"

# Storage Directories for Images
UPLOADS_DIR = AI_DIR / "uploads"
OUTPUT_DIR = AI_DIR / "output"

# Ensure required directories exist at runtime
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# App Configuration Settings
PROJECT_NAME = "FlowSync"
VERSION = "1.0"
STATUS = "Running"

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
