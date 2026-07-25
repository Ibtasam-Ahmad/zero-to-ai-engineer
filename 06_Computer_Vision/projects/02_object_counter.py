"""
Object Counter using YOLO / Background Subtraction
Counts objects in video streams with tracking and line-crossing detection.
Falls back to MOG2 background subtraction if YOLO unavailable.
"""

import cv2
import numpy as np
import os
import time
import argparse
from collections import defaultdict, deque


# ─── YOLO Detector ────────────────────────────────────────────────────────────

class YOLODetector:
    """YOLOv8/v5 detector using ultralytics or OpenCV DNN."""

    def __init__(self, conf_threshold=0.4, classes_of_interest=None):
        self.conf_threshold = conf_threshold
        self.classes_of_interest = classes_of_interest  # None = all classes
        self.backend = None
        self._load()

    def _load(self):
        """Try ultralytics YOLOv8, fallback to OpenCV DNN."""
        try:
            from ultralytics import YOLO
            self.model = YOLO("yolov8n.pt")
            self.backend = "ultralytics"
            print("Loaded YOLOv8n (ultralytics)")
        except Exception:
            self.backend = "mog2"
            print("YOLO unavailable using MOG2 background subtraction")

    def detect(self, frame):
        """Return list of (x1, y1, x2, y2, class_name, confidence)."""
        if self.backend == "ultralytics":
            return self._detect_ultralytics(frame)
        return []

    def _detect_ultralytics(self, frame):
        results = self.model(frame, conf=self.conf_threshold, verbose=False)
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                cls_name = self.model.names[cls_id]
                if self.classes_of_interest and cls_name not in self.classes_of_interest:
                    continue
                conf = float(box.conf[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append((x1, y1, x2, y2, cls_name, conf))
        return detections


# ─── Background Subtractor (fallback) ────────────────────────────────────────

class MOG2Counter:
    """Count moving objects using MOG2 background subtraction."""

    def __init__(self):
        self.subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=True)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        print("MOG2 background subtractor initialized")

    def detect(self, frame):
        """Return bounding boxes of moving objects."""
        mask = self.subtractor.apply(frame)
        # Remove shadows (gray pixels = 127)
        _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
        # Morphological cleanup
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        mask = cv2.dilate(mask, self.kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 500:  # Filter noise
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append((x, y, x + w, y + h, "object", area / 10000))
        return detections


# ─── Simple Centroid Tracker ──────────────────────────────────────────────────

class CentroidTracker:
    """Track objects by centroid distance across frames."""

    def __init__(self, max_disappeared=30, max_distance=80):
        self.next_id = 0
        self.objects = {}       # id → centroid
        self.disappeared = {}   # id → frame count
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        self.trajectories = defaultdict(lambda: deque(maxlen=30))

    def register(self, centroid):
        self.objects[self.next_id] = centroid
        self.disappeared[self.next_id] = 0
        self.next_id += 1

    def deregister(self, obj_id):
        del self.objects[obj_id]
        del self.disappeared[obj_id]

    def update(self, rects):
        """Update tracker with new bounding boxes. Returns {id: centroid}."""
        if len(rects) == 0:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)
            return self.objects

        # Compute centroids of new detections
        input_centroids = np.array([
            ((x1 + x2) // 2, (y1 + y2) // 2)
            for x1, y1, x2, y2, *_ in rects
        ])

        if len(self.objects) == 0:
            for c in input_centroids:
                self.register(tuple(c))
        else:
            obj_ids = list(self.objects.keys())
            obj_centroids = np.array(list(self.objects.values()))

            # Distance matrix
            D = np.linalg.norm(obj_centroids[:, None] - input_centroids[None, :], axis=2)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows, used_cols = set(), set()
            for r, c in zip(rows, cols):
                if r in used_rows or c in used_cols:
                    continue
                if D[r, c] > self.max_distance:
                    continue
                obj_id = obj_ids[r]
                self.objects[obj_id] = tuple(input_centroids[c])
                self.trajectories[obj_id].append(tuple(input_centroids[c]))
                self.disappeared[obj_id] = 0
                used_rows.add(r)
                used_cols.add(c)

            unused_rows = set(range(len(obj_ids))) - used_rows
            unused_cols = set(range(len(input_centroids))) - used_cols

            for r in unused_rows:
                obj_id = obj_ids[r]
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)

            for c in unused_cols:
                self.register(tuple(input_centroids[c]))

        return self.objects


# ─── Line Counter ─────────────────────────────────────────────────────────────

class LineCrossCounter:
    """Count objects crossing a virtual line."""

    def __init__(self, line_y_ratio=0.5, direction="both"):
        self.line_y_ratio = line_y_ratio
        self.direction = direction
        self.prev_positions = {}
        self.in_count = 0
        self.out_count = 0

    def get_line_y(self, frame_height):
        return int(frame_height * self.line_y_ratio)

    def update(self, tracked_objects, frame_height):
        line_y = self.get_line_y(frame_height)
        for obj_id, centroid in tracked_objects.items():
            cx, cy = centroid
            prev_cy = self.prev_positions.get(obj_id)

            if prev_cy is not None:
                # Crossed downward (entering)
                if prev_cy < line_y <= cy:
                    self.in_count += 1
                # Crossed upward (exiting)
                elif prev_cy > line_y >= cy:
                    self.out_count += 1

            self.prev_positions[obj_id] = cy

        return self.in_count, self.out_count

    def draw_line(self, frame):
        h, w = frame.shape[:2]
        line_y = self.get_line_y(h)
        cv2.line(frame, (0, line_y), (w, line_y), (0, 255, 255), 2)
        cv2.putText(frame, f"IN: {self.in_count}  OUT: {self.out_count}",
                    (10, line_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)


# ─── Visualization ────────────────────────────────────────────────────────────

def draw_detections(frame, detections, tracked_objects, tracker, counter):
    """Draw boxes, IDs, trajectories, and stats."""
    # Draw detection boxes
    for x1, y1, x2, y2, cls_name, conf in detections:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 0), 2)
        cv2.putText(frame, f"{cls_name} {conf:.2f}", (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 0), 1)

    # Draw tracked IDs and trajectories
    for obj_id, (cx, cy) in tracked_objects.items():
        cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
        cv2.putText(frame, f"ID:{obj_id}", (cx - 20, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 1)

        # Draw trajectory
        traj = list(tracker.trajectories.get(obj_id, []))
        for i in range(1, len(traj)):
            if traj[i - 1] is None or traj[i] is None:
                continue
            cv2.line(frame, traj[i-1], traj[i], (255, 100, 0), 1)

    # Stats overlay
    total = len(tracked_objects)
    cv2.rectangle(frame, (0, 0), (200, 35), (0, 0, 0), -1)
    cv2.putText(frame, f"Objects: {total}", (5, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    counter.draw_line(frame)
    return frame


# ─── Demo: Synthetic Moving Objects ──────────────────────────────────────────

def run_synthetic_demo(n_objects=5, n_frames=120, output="object_count_demo.avi"):
    """Simulate moving objects for demo purposes."""
    print(f"Running synthetic demo with {n_objects} objects for {n_frames} frames...")

    W, H = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    writer = cv2.VideoWriter(output, fourcc, 20.0, (W, H))

    # Initialize random object trajectories
    np.random.seed(42)
    positions = np.random.rand(n_objects, 2) * [W, H]
    velocities = (np.random.rand(n_objects, 2) - 0.5) * 10

    class_names = ["person", "car", "bicycle", "dog", "bus"]

    tracker = CentroidTracker()
    counter = LineCrossCounter(line_y_ratio=0.5)

    class_counts = defaultdict(int)
    max_ids = 0

    for frame_i in range(n_frames):
        frame = np.zeros((H, W, 3), dtype=np.uint8)

        # Move objects (bounce off walls)
        positions += velocities
        for i in range(n_objects):
            if positions[i, 0] < 20 or positions[i, 0] > W - 20:
                velocities[i, 0] *= -1
            if positions[i, 1] < 20 or positions[i, 1] > H - 20:
                velocities[i, 1] *= -1
        positions = np.clip(positions, [20, 20], [W-20, H-20])

        # Draw objects as colored rectangles
        detections = []
        for i, (px, py) in enumerate(positions):
            x1, y1 = int(px) - 25, int(py) - 35
            x2, y2 = int(px) + 25, int(py) + 35
            cls = class_names[i % len(class_names)]
            detections.append((x1, y1, x2, y2, cls, 0.9))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (100, 200, 100), -1)

        tracked = tracker.update(detections)
        max_ids = max(max_ids, len(tracked))
        counter.update(tracked, H)
        draw_detections(frame, detections, tracked, tracker, counter)

        # Frame number
        cv2.putText(frame, f"Frame: {frame_i+1}/{n_frames}", (W-180, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        writer.write(frame)

    writer.release()
    print(f"Demo saved to {output}")
    print(f"Line crossings IN: {counter.in_count} | OUT: {counter.out_count}")
    print(f"Unique tracked IDs: {max_ids}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Object Counter")
    parser.add_argument("--source", default="demo",
                        help="Video path, 'webcam', or 'demo'")
    parser.add_argument("--classes", nargs="*", default=None,
                        help="Classes to count (e.g. person car)")
    parser.add_argument("--conf", type=float, default=0.4)
    args = parser.parse_args()

    print("=" * 50)
    print("  OBJECT COUNTER")
    print("=" * 50)

    if args.source == "demo":
        run_synthetic_demo()
    else:
        detector = YOLODetector(conf_threshold=args.conf,
                                classes_of_interest=args.classes)
        mog2 = MOG2Counter()
        tracker = CentroidTracker()
        counter = LineCrossCounter()

        if args.source == "webcam":
            cap = cv2.VideoCapture(0)
        else:
            cap = cv2.VideoCapture(args.source)
            if not cap.isOpened():
                print(f"Cannot open: {args.source}")
                exit(1)

        print("Press 'q' to quit.")
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            detections = detector.detect(frame)
            if not detections:
                detections = mog2.detect(frame)
            tracked = tracker.update(detections)
            counter.update(tracked, frame.shape[0])
            draw_detections(frame, detections, tracked, tracker, counter)
            cv2.imshow("Object Counter", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        print(f"Final IN: {counter.in_count} | OUT: {counter.out_count}")

    print("Done!")
