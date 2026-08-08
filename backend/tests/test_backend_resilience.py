import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.services.ai_service import AIService
from backend.ai.learning.logger import get_history_log_path
from backend.app.config import YOLO_MODEL_PATH, LOGS_DIR


def test_ai_service_handles_missing_image_path():
    service = AIService()
    with pytest.raises(FileNotFoundError, match="Input image file not found"):
        service.process_traffic_analysis(Path("does-not-exist.jpg"))


def test_history_log_path_is_under_backend_ai_logs():
    log_path = get_history_log_path()
    assert log_path.endswith("traffic_history.csv")
    assert "backend" in log_path.lower()


def test_app_config_points_to_existing_yolo_weights():
    assert YOLO_MODEL_PATH.exists(), f"Expected YOLO weights at {YOLO_MODEL_PATH}"
    assert LOGS_DIR.exists()
