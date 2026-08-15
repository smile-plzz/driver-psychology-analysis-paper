import time
import yaml
import click
from src.ingest import VideoIngestor
from src.detector import VehicleTracker
from src.psychology import DriverPsychologyEngine
from src.storage import PsychologyDatabase
from src.report import PsychologyReportGenerator

def load_config(config_path: str = "config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@click.group()
def cli():
    """Driver Psychology & Traffic Behavior Computer Vision Pipeline"""
    pass

@cli.command()
@click.option("--source", default=None, help="Video source: 'mock', webcam index '0', RTSP URL, or video path.")
@click.option("--frames", default=30, help="Number of frames/samples to analyze in this run.")
def run(source, frames):
    """Run real-time or synthetic driver psychology tracking pipeline."""
    cfg = load_config()
    source_type = source if source else cfg["camera"]["source"]
    
    print(f"🚀 Starting Driver Psychology Pipeline [Source: {source_type}]...")
    ingestor = VideoIngestor(source=source_type, fps_sample_rate=cfg["camera"]["fps_sample_rate"])
    tracker = VehicleTracker(mode="mock" if source_type == "mock" else "real")
    db = PsychologyDatabase(db_path=cfg["storage"]["db_path"])
    
    ingestor.connect()
    frame_count = 0
    
    try:
        for ts, frame in ingestor.frames():
            detections = tracker.detect_and_track(frame, ts)
            psychology = DriverPsychologyEngine.calculate_window_psychology(detections)
            db.log_metrics(psychology, timestamp=ts)
            
            print(f"[{time.strftime('%H:%M:%S', time.localtime(ts))}] Vehicles: {psychology['total_vehicles']} | "
                  f"Avg Aggression: {psychology['avg_aggression']:.1f}/100 | "
                  f"Behavior: {psychology['dominant_behavior']}")
            
            frame_count += 1
            if frame_count >= frames:
                break
    finally:
        ingestor.release()
        
    print(f"\n✅ Processing complete. {frame_count} windows logged to SQLite DB.")

@cli.command()
def report():
    """Generate a Markdown driver psychology report from SQLite logs."""
    cfg = load_config()
    db = PsychologyDatabase(db_path=cfg["storage"]["db_path"])
    reporter = PsychologyReportGenerator(db)
    report_file = reporter.generate_markdown_report()
    print(f"📄 Report successfully generated at: {report_file}")

if __name__ == "__main__":
    cli()
