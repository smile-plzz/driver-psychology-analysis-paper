import cv2
import time
import numpy as np
from typing import Generator, Tuple, Optional

class VideoIngestor:
    def __init__(self, source: str = "mock", fps_sample_rate: int = 1):
        self.source = source
        self.fps_sample_rate = fps_sample_rate
        self.cap = None

    def connect(self):
        if self.source == "mock":
            print("[Ingest] Initializing Synthetic Mock Video Stream...")
            return
        
        if self.source.isdigit():
            self.cap = cv2.VideoCapture(int(self.source))
        else:
            self.cap = cv2.VideoCapture(self.source)
            
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open video source: {self.source}")

    def frames(self) -> Generator[Tuple[float, np.ndarray], None, None]:
        if self.source == "mock":
            # Generate synthetic frames simulating Dhaka traffic chaos
            frame_idx = 0
            while True:
                timestamp = time.time()
                # Create a blank street canvas (dark asphalt grey)
                img = np.ones((720, 1280, 3), dtype=np.uint8) * 50
                # Draw lane markings
                cv2.line(img, (640, 0), (640, 720), (200, 200, 200), 2, cv2.LINE_AA)
                
                # Yield synthetic frame data
                yield timestamp, img
                frame_idx += 1
                time.sleep(1.0 / self.fps_sample_rate)
        else:
            native_fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
            interval = max(1, int(native_fps / self.fps_sample_rate))
            count = 0
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                if count % interval == 0:
                    yield time.time(), frame
                count += 1

    def release(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
