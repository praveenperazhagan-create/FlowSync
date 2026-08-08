"""
Model Retraining Module
======================

Phase 5: LEARNING AI
Reads `logs/traffic_history.csv`, merges new logged samples with original training dataset,
retrains candidate models, selects the highest accuracy model, and replaces `models/traffic_model.pkl`.
"""

import os
import sys
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
ai_dir = os.path.dirname(current_dir)
if ai_dir not in sys.path:
    sys.path.append(ai_dir)

from training.preprocess import get_default_dataset_path
from training.train import train_and_evaluate_model
from learning.logger import get_history_log_path


def retrain_model() -> bool:
    """
    Merges logged predictions with base dataset and triggers complete model retraining pipeline.
    """
    history_path = get_history_log_path()
    base_dataset_path = get_default_dataset_path()

    print("=" * 60)
    print(" 1. READING TRAFFIC HISTORY LOGS ")
    print("=" * 60)

    if not os.path.exists(history_path) or os.path.getsize(history_path) == 0:
        print("[INFO] No history logs found in `logs/traffic_history.csv`. Proceeding to train on primary dataset.")
    else:
        try:
            df_history = pd.read_csv(history_path)
            print(f"[INFO] Loaded {len(df_history)} logged traffic records from {history_path}.")
            
            # Map history columns to original dataset schema format
            history_mapped = pd.DataFrame()
            history_mapped["timestamp"] = df_history["timestamp"]
            history_mapped["city_zone"] = df_history["city_zone"]
            history_mapped["vehicle_count"] = df_history["vehicle_count"]
            history_mapped["weather_condition"] = df_history["weather"]
            history_mapped["visibility_km"] = df_history["visibility"]
            history_mapped["congestion_level"] = df_history["prediction"]
            history_mapped["signal_cycle_time_sec"] = df_history["recommended_signal_time"]
            history_mapped["avg_wait_time_sec"] = df_history["waiting_time"]

            # Read base dataset and combine
            if os.path.exists(base_dataset_path):
                df_base = pd.read_csv(base_dataset_path)
                df_combined = pd.concat([df_base, history_mapped], ignore_index=True)
                df_combined.to_csv(base_dataset_path, index=False)
                print(f"[SUCCESS] Merged {len(df_history)} new records into main dataset: {base_dataset_path} (Total shape: {df_combined.shape}).")
        except Exception as e:
            print(f"[WARNING] History log merging encountered an issue: {e}. Proceeding with base training.")

    print("\n" + "=" * 60)
    print(" 2. TRIGGERING MODEL RETRAINING & EVALUATION ")
    print("=" * 60)

    best_model, metrics = train_and_evaluate_model()

    print("\n" + "=" * 60)
    print(f" RETRAINING COMPLETE — Best Model Accuracy: {metrics['accuracy']*100:.2f}% ")
    print("=" * 60)

    return True


if __name__ == "__main__":
    retrain_model()
