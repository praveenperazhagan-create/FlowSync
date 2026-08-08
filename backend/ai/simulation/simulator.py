"""
Traffic Signal Simulator
========================

Mathematical traffic simulation engine (Phase 3: SIMULATION AI).
Evaluates multiple traffic signal timing scenarios (e.g., 40s, 60s, 80s, 100s)
without machine learning models.

Uses realistic traffic flow mechanics, queue accumulation models,
and delay functions to compute queue length, average waiting time,
average speed, traffic score, and traffic reduction.
"""

import math
from typing import List, Dict, Any


def simulate_signal_scenarios(
    vehicle_count: int,
    avg_speed_kmph: float = 40.0,
    weather_condition: str = "Clear",
    visibility_km: float = 10.0,
    incident_reported: bool = False,
    signal_timings: List[int] = None
) -> List[Dict[str, Any]]:
    """
    Simulates traffic scenarios for specified signal cycle durations.

    Parameters:
        vehicle_count (int): Total vehicle count detected.
        avg_speed_kmph (float): Current baseline average vehicle speed in km/h.
        weather_condition (str): Weather condition (e.g. Clear, Rain, Fog).
        visibility_km (float): Visibility distance in kilometers.
        incident_reported (bool): Flag indicating active traffic incident.
        signal_timings (List[int], optional): List of green signal times in seconds to test.
                                              Defaults to [40, 60, 80, 100].

    Returns:
        List[Dict[str, Any]]: Array of evaluated scenario results:
            [
                {
                    "signal_time": int,
                    "queue": int,
                    "waiting_time": float,
                    "average_speed": float,
                    "traffic_reduction": float,
                    "traffic_score": float
                },
                ...
            ]
    """
    if signal_timings is None:
        signal_timings = [40, 60, 80, 100]

    # Environmental & Incident friction factors
    weather_lower = weather_condition.lower()
    if weather_lower in ["rain", "heavy rain", "snow", "storm"]:
        weather_factor = 1.25
    elif weather_lower in ["fog", "haze"]:
        weather_factor = 1.15
    else:
        weather_factor = 1.0

    if visibility_km < 3.0:
        visibility_factor = 1.20
    elif visibility_km < 6.0:
        visibility_factor = 1.10
    else:
        visibility_factor = 1.0

    incident_factor = 1.35 if incident_reported else 1.0

    # Total demand multiplier
    friction_multiplier = weather_factor * visibility_factor * incident_factor

    # Assume standard intersection capacity: 0.5 vehicles discharged per second of green time per lane (2 lanes = 1 veh/s)
    discharge_rate_per_sec = 0.95 / friction_multiplier

    scenarios = []

    # Baseline unmanaged scenario (assuming default 60s signal timing)
    baseline_green = 60
    baseline_discharged = baseline_green * discharge_rate_per_sec
    baseline_queue = max(5, int((vehicle_count - baseline_discharged) * 1.1))

    for green_time in signal_timings:
        # Effective discharge during green cycle
        discharged_vehicles = green_time * discharge_rate_per_sec

        # Residual queue calculation
        raw_queue = max(0.0, vehicle_count - discharged_vehicles)
        # Add arrival accumulation rate (0.25 veh/s arriving during red phase)
        red_phase = max(10, 120 - green_time)
        accumulated_queue = raw_queue + (0.25 * red_phase * friction_multiplier)

        final_queue = int(round(max(2, accumulated_queue)))

        # Average waiting time (Webster's delay model simplified approximation)
        # Delay (s) = 0.5 * C * (1 - g/C)^2 / (1 - min(0.95, x) * g/C)
        cycle_time = max(green_time + 30, 90)
        green_ratio = green_time / cycle_time
        degree_of_sat = min(1.2, vehicle_count / max(1.0, discharged_vehicles))
        
        base_delay = 0.5 * cycle_time * ((1.0 - green_ratio) ** 2)
        congestion_delay = 15.0 * (degree_of_sat ** 2) * friction_multiplier
        avg_wait_time = round(base_delay + congestion_delay, 1)

        # Estimated average speed improvement based on queue clearance
        speed_impact = max(5.0, min(65.0, avg_speed_kmph + (green_time * 0.25) - (final_queue * 0.15)))
        estimated_avg_speed = round(speed_impact, 1)

        # Traffic reduction percentage relative to baseline queue
        queue_reduction = ((baseline_queue - final_queue) / max(1, baseline_queue)) * 100.0
        traffic_reduction = round(max(-20.0, min(85.0, queue_reduction)), 1)

        # Overall Traffic Score (0 to 100, higher is better)
        # Balance between low queue, low wait time, high speed, and appropriate signal cycle
        queue_penalty = min(40.0, final_queue * 0.25)
        wait_penalty = min(35.0, avg_wait_time * 0.35)
        speed_bonus = min(25.0, estimated_avg_speed * 0.4)

        raw_score = 100.0 - queue_penalty - wait_penalty + speed_bonus
        traffic_score = round(max(10.0, min(99.0, raw_score)), 1)

        scenarios.append({
            "signal_time": int(green_time),
            "queue": final_queue,
            "waiting_time": avg_wait_time,
            "average_speed": estimated_avg_speed,
            "traffic_reduction": traffic_reduction,
            "traffic_score": traffic_score
        })

    return scenarios


if __name__ == "__main__":
    print("=" * 60)
    print(" TRAFFIC SIMULATION ENGINE DEMO ")
    print("=" * 60)

    results = simulate_signal_scenarios(
        vehicle_count=150,
        avg_speed_kmph=25.0,
        weather_condition="Rain",
        visibility_km=5.0,
        incident_reported=False
    )

    import json
    print(json.dumps(results, indent=2))
