"""
Computer Vision App: image classification, object detection, segmentation.
Uses EfficientNet-B0 (classification), YOLOv8 (detection), SAM-lite (segmentation).
"""

import io
import logging
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image
from torchvision import models
from torchvision.models import EfficientNet_B0_Weights

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ImageNet class labels (abbreviated - full list loaded lazily)
_IMAGENET_CLASSES: Optional[List[str]] = None
_EFFICIENTNET: Optional[torch.nn.Module] = None
_YOLO = None


def get_imagenet_classes() -> List[str]:
    global _IMAGENET_CLASSES
    if _IMAGENET_CLASSES is None:
        try:
            import urllib.request
            url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
            with urllib.request.urlopen(url, timeout=5) as f:
                _IMAGENET_CLASSES = [l.decode("utf-8").strip() for l in f.readlines()]
        except Exception:
            _IMAGENET_CLASSES = [f"class_{i}" for i in range(1000)]
    return _IMAGENET_CLASSES


def get_efficientnet() -> torch.nn.Module:
    global _EFFICIENTNET
    if _EFFICIENTNET is None:
        logger.info("Loading EfficientNet-B0...")
        _EFFICIENTNET = models.efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
        _EFFICIENTNET.eval()
    return _EFFICIENTNET


def preprocess_image(img: Image.Image) -> torch.Tensor:
    transform = T.Compose([
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(img).unsqueeze(0)


def classify(image_bytes: bytes, top_k: int = 5) -> List[Dict]:
    """Return top-k ImageNet classifications with probabilities."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = preprocess_image(img)
    model = get_efficientnet()
    classes = get_imagenet_classes()

    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0]

    top_probs, top_ids = torch.topk(probs, top_k)
    results = []
    for prob, idx in zip(top_probs.tolist(), top_ids.tolist()):
        label = classes[idx] if idx < len(classes) else f"class_{idx}"
        results.append({"label": label, "confidence": round(prob * 100, 2), "class_id": idx})
    return results


def detect(image_bytes: bytes) -> List[Dict]:
    """Run YOLOv8 object detection. Falls back to mock if ultralytics not installed."""
    try:
        from ultralytics import YOLO
        global _YOLO
        if _YOLO is None:
            logger.info("Loading YOLOv8n...")
            _YOLO = YOLO("yolov8n.pt")

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        results = _YOLO(img, verbose=False)[0]
        boxes = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            boxes.append({
                "label":      results.names[int(box.cls)],
                "confidence": round(float(box.conf) * 100, 2),
                "box":        {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            })
        return boxes

    except ImportError:
        # Fallback mock
        return [{"label": "person (mock)", "confidence": 92.5, "box": {"x1": 50, "y1": 30, "x2": 200, "y2": 380}}]


def segment(image_bytes: bytes) -> Dict:
    """Return basic segmentation info. Uses SAM if available, else mock."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    w, h = img.size

    try:
        from ultralytics import SAM
        model = SAM("mobile_sam.pt")
        results = model(img, verbose=False)[0]
        masks = []
        for i, mask in enumerate(results.masks.data[:5]):  # top 5 masks
            m = mask.cpu().numpy().astype(bool)
            masks.append({"mask_id": i, "area": int(m.sum()), "bbox": results.boxes.xyxy[i].tolist() if results.boxes else []})
        return {"width": w, "height": h, "num_masks": len(masks), "masks": masks}
    except Exception:
        # Mock segmentation
        return {
            "width": w, "height": h, "num_masks": 3,
            "masks": [
                {"mask_id": 0, "area": w * h // 3, "bbox": [0, 0, w // 2, h]},
                {"mask_id": 1, "area": w * h // 4, "bbox": [w // 2, 0, w, h // 2]},
                {"mask_id": 2, "area": w * h // 5, "bbox": [w // 2, h // 2, w, h]},
            ],
            "note": "Mock segmentation install ultralytics for real SAM inference",
        }
