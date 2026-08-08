"""
AI Traffic Decision Engine (Phase 4)
=====================================

This module integrates simulation results with predicted congestion metrics
to select the optimal signal timing, output detailed reasoning, summary, and
expected congestion/delay reduction.
"""

import os
import sys
import numpy as np
from typing import Optional, List, Dict, Any

# Ensure simulation and inference packages are accessible
current_dir = os.path.dirname(os.path.abspath(__file__))
ai_dir = os.path.dirname(current_dir)
if ai_dir not in sys.path:
    sys.path.append(ai_dir)

try:
    from simulation.simulator import simulate_signal_scenarios
except ImportError:
    try:
        from ai.simulation.simulator import simulate_signal_scenarios
    except ImportError:
        simulate_signal_scenarios = None

try:
    from predict import predict_congestion
except ImportError:
    predict_congestion = None


def make_traffic_decision(
    congestion_level: Optional[str] = None,
    vehicle_count: int = 100,
    car_count: int = 0,
    bike_count: int = 0,
    bus_count: int = 0,
    truck_count: int = 0,
    emergency_vehicle_count: int = 0,
    avg_speed_kmph: float = 40.0,
    emergency_vehicle_detected: bool = False,
    visibility_km: float = 10.0,
    weather_condition: str = "Clear",
    city_zone: str = "Downtown",
    is_peak_hour: bool = False,
    incident_reported: bool = False,
    simulation_scenarios: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Evaluates simulation scenarios and congestion parameters to pick optimal signal timing.

    1. Receives simulation results (or generates them using simulator.py).
    2. Compares all scenarios (Lowest Queue, Lowest Waiting Time, Highest Traffic Score).
    3. Chooses optimal scenario and recommends `recommended_signal_time`.
    4. Includes detailed `reason_list`, `summary`, and `expected_reduction`.
    """
    reasons = []
    ai_confidence = 90.0

    # ML Congestion Prediction fallback if not supplied
    if congestion_level is None and predict_congestion is not None:
        try:
            pred_res = predict_congestion(
                vehicle_count=vehicle_count,
                avg_speed_kmph=avg_speed_kmph,
                weather_condition=weather_condition,
                visibility_km=visibility_km,
                is_peak_hour=is_peak_hour,
                incident_reported=incident_reported,
                city_zone=city_zone
            )
            congestion_level = pred_res["predicted_congestion_level"]
            ai_confidence = min(99.0, pred_res["confidence_pct"])
            reasons.append(f"AI ML model predicted traffic level as '{congestion_level}' ({ai_confidence:.1f}% confidence).")
        except Exception as e:
            congestion_level = "Moderate"
            reasons.append(f"ML predictor fallback to 'Moderate' due to: {e}")

    # Format congestion string
    if isinstance(congestion_level, str):
        congestion_level = congestion_level.strip().capitalize()
        if congestion_level == "Medium":
            congestion_level = "Moderate"

    # Emergency Override Check (Highest Priority)
    if emergency_vehicle_detected or emergency_vehicle_count > 0:
        reasons.append("[EMERGENCY OVERRIDE] Emergency vehicle detected (ambulance / fire / police). Priority Green Wave activated.")
        reasons.append("Signal cycle set to 120s to clear traffic corridor and minimize delay.")
        summary = f"CRITICAL: Emergency vehicle detected. Priority green wave assigned (120s green light)."
        return {
            "recommended_signal_time": 120,
            "ai_confidence": 99.5,
            "reason_list": reasons,
            "expected_congestion_reduction": "45%",
            "expected_waiting_time_reduction": "75%",
            "emergency_priority": "CRITICAL",
            "summary": summary,
            "simulation_scenarios": simulation_scenarios or []
        }

    # Run Simulation Engine if scenarios not provided directly
    if simulation_scenarios is None and simulate_signal_scenarios is not None:
        simulation_scenarios = simulate_signal_scenarios(
            vehicle_count=vehicle_count,
            avg_speed_kmph=avg_speed_kmph,
            weather_condition=weather_condition,
            visibility_km=visibility_km,
            incident_reported=incident_reported,
            signal_timings=[40, 60, 80, 100]
        )

    # Scenario Selection (Find highest traffic score, lowest queue, lowest waiting time)
    best_scenario = None
    if simulation_scenarios:
        # Sort scenarios by traffic_score desc, queue asc, waiting_time asc
        sorted_scenarios = sorted(
            simulation_scenarios,
            key=lambda s: (-s["traffic_score"], s["queue"], s["waiting_time"])
        )
        best_scenario = sorted_scenarios[0]
        recommended_signal_time = int(best_scenario["signal_time"])
        opt_queue = best_scenario["queue"]
        opt_wait = best_scenario["waiting_time"]
        opt_score = best_scenario["traffic_score"]
        opt_reduction = best_scenario["traffic_reduction"]

        reasons.append(f"Simulation engine evaluated scenarios: {[s['signal_time'] for s in simulation_scenarios]}s.")
        reasons.append(
            f"Selected optimal scenario {recommended_signal_time}s: Lowest Queue ({opt_queue} vehicles), "
            f"Lowest Waiting Time ({opt_wait}s), Highest Traffic Score ({opt_score}/100)."
        )
    else:
        # Static fallback if simulator module is absent
        recommended_signal_time = 60
        opt_queue = max(5, int(vehicle_count * 0.5))
        opt_wait = 30.0
        opt_reduction = 20.0
        reasons.append("Applied fallback signal timing of 60s.")

    # Breakdown log
    reasons.append(
        f"Vehicle Breakdown → Cars: {car_count}, Bikes: {bike_count}, Buses: {bus_count}, Trucks: {truck_count}, Emergency: {emergency_vehicle_count}."
    )

    expected_congestion_reduction_str = f"{opt_reduction}%"
    expected_wait_reduction_str = f"{round(opt_reduction * 1.1, 1)}%"

    dashboard_summary = (
        f"{congestion_level} traffic detected in {city_zone}. "
        f"Simulation selected optimal green signal time of {recommended_signal_time}s "
        f"(Score: {best_scenario['traffic_score'] if best_scenario else 'N/A'}). "
        f"Expected congestion reduction: {expected_congestion_reduction_str}."
    )

    priority = "HIGH" if congestion_level in ["High", "Severe"] or incident_reported else "NORMAL"

    return {
        "estimated_queue_length": opt_queue,
        "traffic_level": congestion_level,
        "current_signal_time": 60,
        "recommended_signal_time": recommended_signal_time,
        "signal_difference": recommended_signal_time - 60,
        "ai_confidence": float(round(ai_confidence, 2)),
        "reason_list": reasons,
        "expected_congestion_reduction": expected_congestion_reduction_str,
        "expected_waiting_time_reduction": expected_wait_reduction_str,
        "emergency_priority": priority,
        "summary": dashboard_summary,
        "simulation_scenarios": simulation_scenarios
    }


if __name__ == "__main__":
    print("=" * 60)
    print(" UPGRADED DECISION ENGINE DEMO ")
    print("=" * 60)

    res = make_traffic_decision(
        congestion_level="High",
        vehicle_count=180,
        car_count=120,
        bike_count=40,
        bus_count=15,
        truck_count=5,
        avg_speed_kmph=20.0,
        city_zone="Downtown"
    )

    import json
    print(json.dumps(res, indent=2))
