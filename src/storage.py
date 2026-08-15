import sqlite3
import os
import json
import time
from typing import Dict, Any, List

class PsychologyDatabase:
    def __init__(self, db_path: str = "data/traffic_psychology.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS psychology_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp REAL,
                    total_vehicles INTEGER,
                    avg_aggression REAL,
                    gap_closing_ratio REAL,
                    cng_aggression REAL,
                    bike_aggression REAL,
                    bus_aggression REAL,
                    dominant_behavior TEXT,
                    class_counts_json TEXT
                )
            """)
            conn.commit()

    def log_metrics(self, metrics: Dict[str, Any], timestamp: float = None):
        if timestamp is None:
            timestamp = time.time()
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO psychology_logs (
                    timestamp, total_vehicles, avg_aggression, gap_closing_ratio,
                    cng_aggression, bike_aggression, bus_aggression, dominant_behavior, class_counts_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp,
                metrics.get("total_vehicles", 0),
                metrics.get("avg_aggression", 0.0),
                metrics.get("gap_closing_ratio", 0.0),
                metrics.get("cng_avg_aggression", 0.0),
                metrics.get("bike_avg_aggression", 0.0),
                metrics.get("bus_avg_aggression", 0.0),
                metrics.get("dominant_behavior", "Unknown"),
                json.dumps(metrics.get("class_counts", {}))
            ))
            conn.commit()

    def fetch_recent_summary(self, limit: int = 50) -> List[Dict[str, Any]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM psychology_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
