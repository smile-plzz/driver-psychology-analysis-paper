import numpy as np
import random
from typing import List, Dict, Any

class VehicleTracker:
    def __init__(self, mode: str = "mock"):
        self.mode = mode
        self.classes = ["cng_autorickshaw", "motorcycle", "bus", "private_sedan", "truck"]
        self.mock_track_id = 1000

    def detect_and_track(self, frame: np.ndarray, timestamp: float) -> List[Dict[str, Any]]:
        detections = []
        
        if self.mode == "mock":
            # Generate realistic synthetic traffic detections for testing
            num_vehicles = random.randint(4, 12)
            for _ in range(num_vehicles):
                cls = random.choices(
                    self.classes, 
                    weights=[0.35, 0.30, 0.10, 0.20, 0.05]
                )[0]
                
                # Mock bounding box
                x1 = random.randint(50, 1100)
                y1 = random.randint(50, 600)
                w = random.randint(40, 120)
                h = random.randint(40, 150)
                
                # Behavioral telemetry
                speed = random.uniform(2.0, 35.0) # pixels/sec
                gap_distance = random.uniform(5.0, 120.0) # pixels
                lane_deviation = random.uniform(0.0, 45.0) # pixels off center
                
                # Psychological indices
                aggression_score = min(100.0, (speed * 1.5) + (max(0, 50 - gap_distance) * 0.8) + (lane_deviation * 0.5))
                is_gap_closing = gap_distance < 30.0 and speed > 15.0
                
                detections.append({
                    "timestamp": timestamp,
                    "track_id": random.randint(1, 50),
                    "vehicle_class": cls,
                    "bbox": [x1, y1, x1+w, y1+h],
                    "speed": speed,
                    "gap_distance": gap_distance,
                    "lane_deviation": lane_deviation,
                    "aggression_score": round(aggression_score, 2),
                    "is_gap_closing": is_gap_closing
                })
        else:
            # Real YOLO integration stub (if actual camera is connected)
            try:
                from ultralytics import YOLO
                # e.g., model = YOLO('yolov8n.pt')
                # results = model(frame)
                pass
            except Exception as e:
                print(f"[Detector] YOLO inference error: {e}")
                
        return detections
