# 🚗 Driver Psychology & Traffic Behavior Analysis

An open computer vision + behavioral telemetry pipeline to analyze urban road driving psychology using window-frame video data. Currently configured to be tested immediately with a **synthetic mock mode**, and ready to plug in a real camera when you install one.

---

## 🧠 What This Actually Measures

This system turns raw video frames into real-time **driver behavior psychology indices**:

| Metric | Psychological Interpretation |
| :--- | :--- |
| **Avg Aggression (0–100)** | Collective driver tension level. High score → aggressive gap-closing, fast unpredictable maneuvers, high-speed weaving. |
| **Gap-Closing Ratio** | Percentage of vehicles that aggressively surge into micro-gaps (index of scarcity mindset / competition for road space). |
| **Vehicle-Class Aggression (CNG/Bike/Bus)** | Broken down by vehicle archetype so you can see which driver sub-culture is driving the psychological state of the road. |
| **Dominant Behavior Tag** | An NLP-style readable label summarizing the current road psychology (e.g., *"High Territorial Aggression & Hyper-Competitive Gap Closing"*). |

---

## 📦 Repo Structure

```text
driver-psychology-analysis/
├── config.yaml             # Pipeline + camera configuration (edit before using with real camera)
├── requirements.txt        # Python dependencies
├── main.py                 # CLI entry point (click commands: run / report)
├── src/
│   ├── ingest.py           # Video stream ingestion + synthetic mock frame generator
│   ├── detector.py         # Vehicle detection/tracking → behavioral telemetry (mock + real YOLO stub)
│   ├── psychology.py       # Raw telemetry → psychology indices + dominant behavior classifier
│   ├── storage.py          # SQLite telemetry database
│   └── report.py           # Markdown report generator from DB logs
├── data/                   # Created at runtime (SQLite DB here)
└── reports/                # Generated driver psychology summary files
```

---

## ⚡ Quick Start (Mock Mode Right Now)

You can run the full pipeline immediately without any camera hardware to verify the architecture.

```bash
# 1. Create virtualenv (recommended)
python -m venv .venv
.\.venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run pipeline in mock/synthetic mode (default)
python main.py run --frames 50

# 4. Generate psychology summary report
python main.py report
```

The mock mode simulates realistic Dhaka-style street traffic telemetry (gap-closing events, varying vehicle classes, aggression spikes) so you can see the full end-to-end data flow.

---

## 📷 Plugging In Your Camera (The Final Step)

When the physical camera is installed and streaming, update `config.yaml`:

```yaml
camera:
  source: "mock"                    # ← change this
  # Real source options below:
  # source: "0"                     # e.g. local webcam index
  # source: "rtsp://192.168.1.50:554/stream"
  # source: "/path/to/video_file.mp4"
  fps_sample_rate: 1                # 1 frame/sec recommended for long-term analysis
  resolution: [1280, 720]
  roi: [0, 0, 1280, 720]            # If cropping a screen area, set region of interest
```

Then restart:

```bash
python main.py run --frames 100
```

The detector module currently has a **Real YOLO stub** ready for full YOLOv8 integration when you want to go beyond mock telemetry. `detector.py` includes the integration skeleton (imports ultralytics, reads frame, runs inference). You'll just need to drop in a trained model or label classes specific to your camera's perspective once real video is connected.

---

## 📊 Ongoing Data

Every window analyzed is logged to SQLite in `data/traffic_psychology.db`. You can accumulate data over days/weeks and generate periodic reports to study how driver psychology shifts by time of day, weather, or events.

```bash
python main.py run            # keep it running in background for long-term collection
python main.py report         # generate latest summary markdown
```

---

## 🛠 Next-Level Extensions (Optional Future Work)

- Replace mock telemetry with real YOLOv8 vehicle tracking (`src/detector.py` → full YOLO model integration).
- Add frame-level visualization overlays (bounding boxes + aggression score coloring).
- Add temporal aggregation: hourly/daily aggression heatmaps.
- Connect Telegram/Discord webhook alerts when aggression crosses a critical threshold.

---

Enjoy and let me know when the camera hardware is mounted — that's the moment this gets real. 🏙️📹
