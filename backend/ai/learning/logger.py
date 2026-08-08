"""
Traffic Prediction Logger
=========================

Phase 5: LEARNING AI
Appends every prediction and decision payload to `logs/traffic_history.csv`.
"""

import os
import csv
from datetime import datetime
from typing import Dict, Any


def get_history_log_path() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, "..", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return os.path.abspath(os.path.join(logs_dir, "traffic_history.csv"))


CSV_HEADER = [
    "timestamp",
    "city_zone",
    "vehicle_count",
    "cars",
    "bikes",
    "bus",
    "truck",
    "weather",
    "visibility",
    "prediction",
    "confidence",
    "recommended_signal_time",
    "queue_length",
    "waiting_time"
]


def log_prediction(
    city_zone: str,
    vehicle_count: int,
    cars: int,
    bikes: int,
    bus: int,
    truck: int,
    weather: str,
    visibility: float,
    prediction: str,
    confidence: float,
    recommended_signal_time: int,
    queue_length: int,
    waiting_time: float,
    timestamp: str = None
) -> str:
    """
    Appends a new prediction record to `logs/traffic_history.csv`.
    """
    log_file = get_history_log_path()
    file_exists = os.path.exists(log_file) and os.path.getsize(log_file) > 0

    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        timestamp,
        city_zone,
        vehicle_count,
        cars,
        bikes,
        bus,
        truck,
        weather,
        visibility,
        prediction,
        confidence,
        recommended_signal_time,
        queue_length,
        waiting_time
    ]

    try:
        with open(log_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(CSV_HEADER)
            writer.writerow(row)
        print(f"[LOGGER] Appended prediction log entry to: {log_file}")
    except Exception as e:
        print(f"[LOGGER ERROR] Failed to log prediction entry: {e}")

    return log_file


if __name__ == "__main__":
    log_prediction(
        city_zone="Downtown",
        vehicle_count=140,
        cars=90,
        bikes=30,
        bus=10,
        truck=10,
        weather="Clear",
        visibility=10.0,
        prediction="High",
        confidence=94.5,
        recommended_signal_time=80,
        queue_length=35,
        waiting_time=25.0
    )
