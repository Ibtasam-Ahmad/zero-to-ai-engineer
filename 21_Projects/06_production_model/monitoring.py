"""Prediction logging, drift detection stub, and Prometheus metrics."""

import time
import uuid
from collections import deque
from typing import Deque, Dict, List, Optional

try:
    from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

# Prometheus metrics
if PROMETHEUS_AVAILABLE:
    REQUEST_COUNT   = Counter("predictions_total", "Total predictions", ["model", "label"])
    REQUEST_LATENCY = Histogram("prediction_latency_ms", "Latency in ms", ["model"])
    CONFIDENCE_GAUGE = Gauge("avg_confidence", "Rolling avg confidence", ["model"])

# In-memory log (last 1000 predictions)
_prediction_log: Deque[Dict] = deque(maxlen=1000)
_confidence_window: Deque[float] = deque(maxlen=100)


def log_prediction(text: str, result: Dict, request_id: Optional[str] = None):
    # Use the caller's request_id so the id returned to the client matches the log entry
    entry = {
        "request_id": request_id or str(uuid.uuid4())[:8],
        "timestamp":  time.time(),
        "text_len":   len(text),
        "label":      result["label"],
        "confidence": result["confidence"],
        "model":      result["model_version"],
        "latency_ms": result["inference_ms"],
    }
    _prediction_log.append(entry)
    _confidence_window.append(result["confidence"])

    if PROMETHEUS_AVAILABLE:
        REQUEST_COUNT.labels(model=result["model_version"], label=result["label"]).inc()
        REQUEST_LATENCY.labels(model=result["model_version"]).observe(result["inference_ms"])
        avg = sum(_confidence_window) / len(_confidence_window)
        CONFIDENCE_GAUGE.labels(model=result["model_version"]).set(avg)


def get_metrics_summary() -> Dict:
    if not _prediction_log:
        return {"total_predictions": 0}
    logs = list(_prediction_log)
    total   = len(logs)
    pos     = sum(1 for l in logs if l["label"] == "positive")
    avg_lat = sum(l["latency_ms"] for l in logs) / total
    avg_con = sum(l["confidence"] for l in logs) / total
    return {
        "total_predictions": total,
        "positive_rate":     round(pos / total, 3),
        "negative_rate":     round(1 - pos / total, 3),
        "avg_latency_ms":    round(avg_lat, 2),
        "avg_confidence":    round(avg_con, 2),
        "recent":            logs[-5:][::-1],
    }


def check_drift() -> Dict:
    """Simple confidence drift detection stub."""
    if len(_confidence_window) < 20:
        return {"drift_detected": False, "reason": "Insufficient data"}
    avg = sum(_confidence_window) / len(_confidence_window)
    drift = avg < 70.0  # flag if avg confidence drops below 70%
    return {
        "drift_detected":    drift,
        "avg_confidence":    round(avg, 2),
        "threshold":         70.0,
        "recommendation":    "Consider retraining" if drift else "Model healthy",
    }


def get_prometheus_metrics():
    if PROMETHEUS_AVAILABLE:
        return generate_latest(), CONTENT_TYPE_LATEST
    return b"# Prometheus not installed\n", "text/plain"
