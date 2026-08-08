"""
Traffic Congestion Prediction Script
====================================

This script loads the trained model from `models/traffic_model.pkl` and saved label encoders
from `models/encoders.pkl` to predict `congestion_level` along with prediction confidence.

Required Inputs:
- vehicle_count (int/float)
- avg_speed_kmph (float)
- weather_condition (str: e.g., 'Clear', 'Rain', 'Fog')
- visibility_km (float)
- is_peak_hour (bool)
- incident_reported (bool)
- city_zone (str: e.g., 'Downtown', 'Suburb', 'Commercial', 'Residential')
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np

CONGESTION_LEVEL_MAP = {
    0: "Low",
    1: "Moderate",
    2: "High",
    3: "Severe"
}

FEATURE_DEFAULTS = {
    "road_name": "Main Street",
    "city_zone": "Downtown",
    "latitude": 13.045,
    "longitude": 80.225,
    "vehicle_count": 100,
    "avg_speed_kmph": 40.0,
    "travel_time_index": 1.15,
    "weather_condition": "Clear",
    "temperature_c": 27.5,
    "humidity_pct": 55.0,
    "visibility_km": 8.0,
    "signal_status": "Green",
    "signal_cycle_time_sec": 60,
    "avg_wait_time_sec": 20.0,
    "incident_reported": False,
    "incident_type": "No Incident",
    "road_closure": False,
    "construction_zone": False,
    "event_nearby": False,
    "is_peak_hour": False,
    "is_weekend": False,
    "is_public_holiday": False,
    "hour": 14,
    "day": 15,
    "month": 6,
    "dayofweek": 2,
    "year": 2026
}


def get_model_path() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(script_dir, "..", "models", "traffic_model.pkl"),
        os.path.join(os.getcwd(), "models", "traffic_model.pkl"),
        os.path.join(os.getcwd(), "ai", "models", "traffic_model.pkl"),
        "traffic_model.pkl"
    ]
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
    return os.path.abspath(possible_paths[0])


def get_encoders_path() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(script_dir, "..", "models", "encoders.pkl"),
        os.path.join(os.getcwd(), "models", "encoders.pkl"),
        os.path.join(os.getcwd(), "ai", "models", "encoders.pkl"),
        "encoders.pkl"
    ]
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return abs_path
    return os.path.abspath(possible_paths[0])


def load_trained_model(model_path: str = None):
    if model_path is None:
        model_path = get_model_path()
        
    print(f"[INFO] Loading model from: {model_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please run train.py first.")
        
    model = joblib.load(model_path)
    print("[SUCCESS] Model loaded successfully.")
    return model


def load_encoders(encoders_path: str = None) -> dict:
    if encoders_path is None:
        encoders_path = get_encoders_path()
    if os.path.exists(encoders_path):
        try:
            encoders = joblib.load(encoders_path)
            return encoders
        except Exception as e:
            print(f"[WARNING] Failed to load encoders from {encoders_path}: {e}")
    return {}


def encode_feature(val: str, col_name: str, encoders: dict) -> int:
    val_str = str(val)
    if col_name in encoders:
        le = encoders[col_name]
        if val_str in le.classes_:
            return int(le.transform([val_str])[0])
        else:
            # Fallback for unseen label using hash modulo classes length
            return int(hash(val_str) % len(le.classes_))
    # General fallback
    fallback_maps = {
        "city_zone": {"Downtown": 0, "Commercial": 1, "Industrial": 2, "Residential": 3, "Suburb": 4},
        "weather_condition": {"Clear": 0, "Cloudy": 1, "Fog": 2, "Haze": 3, "Rain": 4},
        "signal_status": {"Flashing": 0, "Green": 1, "Not Signalized": 2, "Red": 3, "Yellow": 4},
        "incident_type": {"Accident": 0, "Breakdown": 1, "No Incident": 2, "Other": 3}
    }
    if col_name in fallback_maps:
        return fallback_maps[col_name].get(val_str, hash(val_str) % len(fallback_maps[col_name]))
    return hash(val_str) % 100


def prepare_input_features(
    vehicle_count: int,
    avg_speed_kmph: float,
    weather_condition: str,
    visibility_km: float,
    is_peak_hour: bool,
    incident_reported: bool,
    city_zone: str,
    encoders: dict = None,
    **kwargs
) -> pd.DataFrame:
    if encoders is None:
        encoders = load_encoders()

    input_dict = FEATURE_DEFAULTS.copy()

    input_dict.update({
        "vehicle_count": int(vehicle_count),
        "avg_speed_kmph": float(avg_speed_kmph),
        "weather_condition": str(weather_condition),
        "visibility_km": float(visibility_km),
        "is_peak_hour": int(is_peak_hour),
        "incident_reported": int(incident_reported),
        "city_zone": str(city_zone)
    })

    for key, val in kwargs.items():
        if key in input_dict:
            input_dict[key] = val

    if "travel_time_index" not in kwargs:
        input_dict["travel_time_index"] = round(max(1.0, 50.0 / max(avg_speed_kmph, 1.0)), 2)

    # Encode categorical features using saved LabelEncoders
    for cat_col in ["city_zone", "weather_condition", "signal_status", "incident_type", "road_name"]:
        input_dict[cat_col] = encode_feature(input_dict[cat_col], cat_col, encoders)

    for key in ["is_weekend", "is_public_holiday", "road_closure", "construction_zone", "event_nearby"]:
        input_dict[key] = int(bool(input_dict[key]))

    feature_columns = [
        'road_name', 'city_zone', 'latitude', 'longitude', 'vehicle_count',
        'avg_speed_kmph', 'travel_time_index', 'weather_condition', 'temperature_c',
        'humidity_pct', 'visibility_km', 'signal_status', 'signal_cycle_time_sec',
        'avg_wait_time_sec', 'incident_reported', 'incident_type', 'road_closure',
        'construction_zone', 'event_nearby', 'is_peak_hour', 'is_weekend',
        'is_public_holiday', 'hour', 'day', 'month', 'dayofweek', 'year'
    ]

    df_input = pd.DataFrame([input_dict])[feature_columns]
    return df_input


def predict_congestion(
    vehicle_count: int,
    avg_speed_kmph: float,
    weather_condition: str,
    visibility_km: float,
    is_peak_hour: bool,
    incident_reported: bool,
    city_zone: str,
    model=None,
    encoders: dict = None
) -> dict:
    """
    Predicts congestion level and returns prediction confidence.

    Returns:
        dict: {
            "predicted_congestion_level": str,
            "confidence_pct": float,
            "class_probabilities": dict
        }
    """
    if model is None:
        model = load_trained_model()
    if encoders is None:
        encoders = load_encoders()

    input_df = prepare_input_features(
        vehicle_count=vehicle_count,
        avg_speed_kmph=avg_speed_kmph,
        weather_condition=weather_condition,
        visibility_km=visibility_km,
        is_peak_hour=is_peak_hour,
        incident_reported=incident_reported,
        city_zone=city_zone,
        encoders=encoders
    )

    pred_class_idx = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    predicted_label = CONGESTION_LEVEL_MAP.get(pred_class_idx, f"Class {pred_class_idx}")
    confidence_score = float(np.max(probabilities) * 100.0)

    prob_dict = {
        CONGESTION_LEVEL_MAP.get(idx, f"Class {idx}"): float(round(prob * 100, 2))
        for idx, prob in enumerate(probabilities)
    }

    result = {
        "predicted_congestion_level": predicted_label,
        "confidence_pct": round(confidence_score, 2),
        "class_probabilities": prob_dict
    }

    return result


if __name__ == "__main__":
    print("="*60)
    print(" TRAFFIC CONGESTION INFERENCE DEMO ")
    print("="*60)

    scenario_1 = {
        "vehicle_count": 350,
        "avg_speed_kmph": 12.5,
        "weather_condition": "Rain",
        "visibility_km": 3.5,
        "is_peak_hour": True,
        "incident_reported": True,
        "city_zone": "Downtown"
    }
    
    print(f"Inputs: {scenario_1}")
    res1 = predict_congestion(**scenario_1)
    print(f"Prediction : {res1['predicted_congestion_level']}")
    print(f"Confidence : {res1['confidence_pct']}%")
    print(f"Probabilities: {res1['class_probabilities']}")
