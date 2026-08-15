from typing import List, Dict, Any

class DriverPsychologyEngine:
    """
    Translates raw trajectory and proximity telemetry into higher-level
    urban behavioral psychology indices.
    """
    
    @staticmethod
    def calculate_window_psychology(detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not detections:
            return {
                "total_vehicles": 0,
                "avg_aggression": 0.0,
                "gap_closing_ratio": 0.0,
                "class_dominance": {},
                "dominant_behavior": "Quiet / Empty Road"
            }

        total = len(detections)
        avg_aggression = sum(d["aggression_score"] for d in detections) / total
        gap_closers = sum(1 for d in detections if d["is_gap_closing"])
        gap_closing_ratio = gap_closers / total

        # Count vehicle classes
        class_counts = {}
        for d in detections:
            cls = d["vehicle_class"]
            class_counts[cls] = class_counts.get(cls, 0) + 1

        # Class behavioral analysis
        cng_aggression = [d["aggression_score"] for d in detections if d["vehicle_class"] == "cng_autorickshaw"]
        bike_aggression = [d["aggression_score"] for d in detections if d["vehicle_class"] == "motorcycle"]
        bus_aggression = [d["aggression_score"] for d in detections if d["vehicle_class"] == "bus"]

        # Determine dominant road psychological state
        if avg_aggression > 65.0:
            dominant_behavior = "High Territorial Aggression & Hyper-Competitive Gap Closing"
        elif gap_closing_ratio > 0.4:
            dominant_behavior = "Scarcity Mindset / Anxious Bumper-to-Bumper Crawl"
        elif avg_aggression < 30.0:
            dominant_behavior = "Courteous Flow / Low-Stress Traffic"
        else:
            dominant_behavior = "Moderate Competitive Maneuvering"

        return {
            "total_vehicles": total,
            "avg_aggression": round(avg_aggression, 2),
            "gap_closing_ratio": round(gap_closing_ratio, 2),
            "class_counts": class_counts,
            "cng_avg_aggression": round(sum(cng_aggression) / len(cng_aggression), 2) if cng_aggression else 0.0,
            "bike_avg_aggression": round(sum(bike_aggression) / len(bike_aggression), 2) if bike_aggression else 0.0,
            "bus_avg_aggression": round(sum(bus_aggression) / len(bus_aggression), 2) if bus_aggression else 0.0,
            "dominant_behavior": dominant_behavior
        }
