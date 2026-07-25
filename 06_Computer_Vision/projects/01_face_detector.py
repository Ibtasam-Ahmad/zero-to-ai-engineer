"""
Real-Time Face Detection + Emotion/Age/Gender Recognition
Uses OpenCV Haar cascades and optionally DeepFace for attributes.
Can process webcam feed, video file, or image directory.
"""

import cv2
import numpy as np
import os
import sys
import time
import argparse
from pathlib import Path


# ─── Detector ─────────────────────────────────────────────────────────────────

class FaceDetector:
    """Multi-scale face detector using OpenCV DNN + Haar cascade fallback."""

    def __init__(self, method="dnn"):
        self.method = method
        if method == "dnn":
            self._load_dnn_model()
        else:
            self._load_haar()

    def _load_dnn_model(self):
        """Try to load OpenCV DNN face detector (SSD + ResNet)."""
        try:
            proto = cv2.data.haarcascades + "../dnn/opencv_face_detector.pbtxt"
            model = cv2.data.haarcascades + "../dnn/opencv_face_detector_uint8.pb"
            if os.path.exists(proto) and os.path.exists(model):
                self.net = cv2.dnn.readNet(model, proto)
                print("Loaded DNN face detector")
                return
        except Exception:
            pass
        # Fall back to Haar
        self._load_haar()
        self.method = "haar"

    def _load_haar(self):
        """Load Haar cascade classifiers."""
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        eye_path = cv2.data.haarcascades + "haarcascade_eye.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.eye_cascade = cv2.CascadeClassifier(eye_path)
        print(f"Loaded Haar cascade: {cascade_path}")

    def detect(self, frame):
        """Return list of (x, y, w, h) face bounding boxes."""
        if self.method == "haar":
            return self._detect_haar(frame)
        return self._detect_dnn(frame)

    def _detect_haar(self, frame):
        """Haar cascade detection."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5,
            minSize=(40, 40), flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces if len(faces) > 0 else []

    def _detect_dnn(self, frame):
        """DNN-based detection (more robust)."""
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                      (104.0, 177.0, 123.0), swapRB=False)
        self.net.setInput(blob)
        detections = self.net.forward()
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype(int)
                faces.append((x1, y1, x2 - x1, y2 - y1))
        return faces


# ─── Attribute Analysis ───────────────────────────────────────────────────────

def analyze_attributes(face_crop):
    """Use DeepFace for age/gender/emotion. Falls back to mock if unavailable."""
    try:
        from deepface import DeepFace
        result = DeepFace.analyze(face_crop, actions=["emotion", "age", "gender"],
                                   enforce_detection=False, silent=True)
        if isinstance(result, list):
            result = result[0]
        return {
            "emotion": result.get("dominant_emotion", "unknown"),
            "age": result.get("age", 0),
            "gender": result.get("dominant_gender", "unknown"),
        }
    except Exception:
        return {"emotion": "—", "age": "—", "gender": "—"}


# ─── Drawing ──────────────────────────────────────────────────────────────────

def draw_face_info(frame, x, y, w, h, attrs=None, confidence=None, idx=0):
    """Draw bounding box and labels on frame."""
    colors = [(0, 255, 0), (255, 100, 0), (0, 100, 255), (255, 0, 255)]
    color = colors[idx % len(colors)]

    # Bounding box
    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # Confidence
    if confidence:
        cv2.putText(frame, f"{confidence:.2f}", (x, y - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Attribute labels
    if attrs:
        label = (f"Age:{attrs['age']} | "
                 f"{attrs['gender']} | "
                 f"{attrs['emotion']}")
        # Background for text
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.rectangle(frame, (x, y - th - 10), (x + tw + 5, y), color, -1)
        cv2.putText(frame, label, (x + 2, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

    return frame


def overlay_stats(frame, n_faces, fps):
    """Overlay frame stats."""
    info = f"Faces: {n_faces} | FPS: {fps:.1f}"
    cv2.putText(frame, info, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    return frame


# ─── Processing ──────────────────────────────────────────────────────────────

def process_frame(frame, detector, analyze=False):
    """Detect faces in a frame and optionally analyze attributes."""
    faces = detector.detect(frame)
    for i, (x, y, w, h) in enumerate(faces):
        # Clamp to frame bounds
        x, y = max(0, x), max(0, y)
        x2 = min(frame.shape[1], x + w)
        y2 = min(frame.shape[0], y + h)

        attrs = None
        if analyze and (x2 - x) > 40 and (y2 - y) > 40:
            face_crop = frame[y:y2, x:x2]
            attrs = analyze_attributes(face_crop)

        draw_face_info(frame, x, y, w, h, attrs, idx=i)

    return frame, len(faces)


def process_image(image_path, detector, output_dir="face_output", analyze=False):
    """Process a single image file."""
    os.makedirs(output_dir, exist_ok=True)
    img = cv2.imread(image_path)
    if img is None:
        print(f"Cannot read: {image_path}")
        return

    result, n_faces = process_frame(img, detector, analyze)
    out_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(out_path, result)
    print(f"{os.path.basename(image_path)}: {n_faces} face(s) → {out_path}")


def run_webcam(detector, analyze=False, cam_idx=0):
    """Process live webcam stream."""
    cap = cv2.VideoCapture(cam_idx)
    if not cap.isOpened():
        print(f"Cannot open camera {cam_idx}")
        return

    print("Webcam running. Press 'q' to quit, 's' to save frame, 'a' to toggle analysis.")
    fps_buffer = []
    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        result, n_faces = process_frame(frame, detector, analyze)

        # FPS calculation
        now = time.time()
        fps_buffer.append(1.0 / max(now - prev_time, 1e-8))
        prev_time = now
        if len(fps_buffer) > 30:
            fps_buffer.pop(0)
        fps = np.mean(fps_buffer)

        overlay_stats(result, n_faces, fps)
        cv2.imshow("Face Detector", result)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("s"):
            fname = f"capture_{int(time.time())}.jpg"
            cv2.imwrite(fname, result)
            print(f"Saved: {fname}")
        elif key == ord("a"):
            analyze = not analyze
            print(f"Attribute analysis: {'ON' if analyze else 'OFF'}")

    cap.release()
    cv2.destroyAllWindows()


def run_demo_synthetic():
    """Demo on a synthetically generated face-like image."""
    print("Generating synthetic demo image...")
    img = np.ones((480, 640, 3), dtype=np.uint8) * 200

    # Draw a simple "face" shape
    cv2.ellipse(img, (320, 240), (100, 130), 0, 0, 360, (200, 170, 140), -1)
    cv2.circle(img, (280, 200), 20, (80, 60, 40), -1)  # left eye
    cv2.circle(img, (360, 200), 20, (80, 60, 40), -1)  # right eye
    cv2.ellipse(img, (320, 300), (50, 25), 0, 0, 180, (120, 80, 80), -1)  # mouth

    cv2.imwrite("synthetic_face_input.jpg", img)
    return img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face Detector")
    parser.add_argument("--source", default="demo",
                        help="'webcam', image path, image directory, or 'demo'")
    parser.add_argument("--analyze", action="store_true",
                        help="Enable age/gender/emotion analysis (requires DeepFace)")
    parser.add_argument("--method", default="haar", choices=["haar", "dnn"],
                        help="Detection method")
    args = parser.parse_args()

    print("=" * 50)
    print("  FACE DETECTOR")
    print("=" * 50)

    detector = FaceDetector(method=args.method)

    if args.source == "webcam":
        run_webcam(detector, analyze=args.analyze)

    elif args.source == "demo":
        img = run_demo_synthetic()
        result, n_faces = process_frame(img, detector, analyze=args.analyze)
        cv2.imwrite("face_detection_result.jpg", result)
        print(f"Demo complete. Detected {n_faces} face(s). Output: face_detection_result.jpg")
        cv2.imshow("Face Detection Demo", result)
        cv2.waitKey(2000)
        cv2.destroyAllWindows()

    elif os.path.isdir(args.source):
        exts = {".jpg", ".jpeg", ".png", ".bmp"}
        images = [str(p) for p in Path(args.source).iterdir()
                  if p.suffix.lower() in exts]
        print(f"Processing {len(images)} images from {args.source}")
        for img_path in images:
            process_image(img_path, detector, analyze=args.analyze)

    else:
        process_image(args.source, detector, analyze=args.analyze)

    print("Done!")
