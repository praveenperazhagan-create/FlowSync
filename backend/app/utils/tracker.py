"""
Backend Utility Helpers
=======================
"""

import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("FlowSyncBackend")

class MetricsTracker:
    def __init__(self):
        self.images_processed = 0
        self.videos_processed = 0
        self.total_vehicles_detected = 0
        self.total_response_time_ms = 0.0
        self.request_count = 0

    def record_request(self, duration_ms: float, vehicles: int = 0, is_video: bool = False):
        self.request_count += 1
        self.total_response_time_ms += duration_ms
        self.total_vehicles_detected += vehicles
        if is_video:
            self.videos_processed += 1
        else:
            self.images_processed += 1

    @property
    def average_response_time_ms(self) -> float:
        if self.request_count == 0:
            return 0.0
        return round(self.total_response_time_ms / self.request_count, 2)

metrics_tracker = MetricsTracker()
