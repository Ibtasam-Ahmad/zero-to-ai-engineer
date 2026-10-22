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
_SSDLITE = None
_SAM = None


def get_imagenet_classes() -> List[str]:
    global _IMAGENET_CLASSES
    if _IMAGENET_CLASSES is None:
        # torchvision ships the 1,000 class names with the weights, so this works offline too
        _IMAGENET_CLASSES = list(EfficientNet_B0_Weights.DEFAULT.meta["categories"])
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


def detect_ssdlite(img: Image.Image, min_score: float = 0.3) -> List[Dict]:
    """Real fallback detector from torchvision (COCO classes, ~13 MB download, fast on CPU)."""
    global _SSDLITE
    from torchvision.models.detection import SSDLite320_MobileNet_V3_Large_Weights, ssdlite320_mobilenet_v3_large
    weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
    if _SSDLITE is None:
        logger.info("Loading SSDLite320-MobileNetV3 (torchvision)...")
        _SSDLITE = ssdlite320_mobilenet_v3_large(weights=weights).eval()
    with torch.no_grad():
        out = _SSDLITE([weights.transforms()(img)])[0]
    names = weights.meta["categories"]
    return [{"label": names[label], "confidence": round(score * 100, 2),
             "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}}
            for (x1, y1, x2, y2), label, score in zip(out["boxes"].tolist(), out["labels"].tolist(), out["scores"].tolist())
            if score >= min_score]


def detect(image_bytes: bytes) -> Dict:
    """Run YOLOv8 object detection. Falls back to torchvision SSDLite (a real detector, no fake boxes)
    if ultralytics or its weights are not available. Returns {"model": ..., "detections": [...]}."""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    try:
        from ultralytics import YOLO
        global _YOLO
        if _YOLO is None:
            logger.info("Loading YOLOv8n...")
            _YOLO = YOLO("yolov8n.pt")

        results = _YOLO(img, verbose=False)[0]
        boxes = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            boxes.append({
                "label":      results.names[int(box.cls)],
                "confidence": round(float(box.conf) * 100, 2),
                "box":        {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            })
        return {"model": "YOLOv8n (ultralytics)", "detections": boxes}

    except Exception as e:
        logger.warning(f"YOLOv8 not available ({type(e).__name__}); using torchvision SSDLite instead.")
        return {"model": "SSDLite320-MobileNetV3 (torchvision)", "detections": detect_ssdlite(img)}


def segment(image_bytes: bytes, mode: str = "objects") -> Dict:
    """Return segmentation info using MobileSAM.
    mode="objects": detected boxes are the SAM prompts (one mask per object, fast).
    mode="everything": SAM's automatic mode (very slow on a CPU). Mock only if ultralytics is missing."""
    global _SAM
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    w, h = img.size

    try:
        from ultralytics import SAM
        if _SAM is None:
            _SAM = SAM("mobile_sam.pt")  # load once (it used to be reloaded on every request)
        labels = None
        if mode == "objects":
            dets = detect(image_bytes)["detections"]
            if not dets:
                return {"width": w, "height": h, "mode": mode, "num_masks": 0, "masks": [],
                        "note": "No objects detected, so nothing to segment. Try mode=everything (slow)."}
            labels = [d["label"] for d in dets]
            results = _SAM(img, bboxes=[[d["box"][k] for k in ("x1", "y1", "x2", "y2")] for d in dets], verbose=False)[0]
        else:
            results = _SAM(img, verbose=False)[0]
        masks = []
        boxes = results.boxes.xyxy.tolist() if results.boxes is not None else []
        for i, mask in enumerate(results.masks.data if results.masks is not None else []):
            m = mask.cpu().numpy().astype(bool)
            if m.sum() == 0:  # skip empty masks
                continue
            entry = {"area": int(m.sum()), "bbox": boxes[i] if i < len(boxes) else []}
            if labels is not None and i < len(labels):
                entry["label"] = labels[i]
            masks.append(entry)
        masks.sort(key=lambda m: m["area"], reverse=True)  # largest first
        if mode != "objects":
            masks = masks[:5]  # top 5 masks
        for i, m in enumerate(masks):
            m["mask_id"] = i
        return {"width": w, "height": h, "mode": mode, "num_masks": len(masks), "masks": masks}
    except ImportError:
        # Mock segmentation, clearly marked as DEMO (only when ultralytics is not installed)
        return {
            "width": w, "height": h, "mode": "demo", "demo": True, "num_masks": 3,
            "masks": [
                {"mask_id": 0, "area": w * h // 3, "bbox": [0, 0, w // 2, h]},
                {"mask_id": 1, "area": w * h // 4, "bbox": [w // 2, 0, w, h // 2]},
                {"mask_id": 2, "area": w * h // 5, "bbox": [w // 2, h // 2, w, h]},
            ],
            "note": "DEMO ONLY: these are fake rectangles, not a real segmentation. Install ultralytics for real SAM inference",
        }
