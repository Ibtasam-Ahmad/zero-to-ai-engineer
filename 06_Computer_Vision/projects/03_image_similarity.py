"""
Image Similarity Search Engine
Extracts deep features using ResNet/EfficientNet, builds a FAISS index,
and retrieves top-K similar images for a query.
"""

import numpy as np
import os
import json
import time
import argparse
from pathlib import Path
import matplotlib.pyplot as plt

# ─── Feature Extractor ────────────────────────────────────────────────────────

class FeatureExtractor:
    """Extract embeddings using a pretrained CNN backbone."""

    def __init__(self, model_name="resnet50", device=None):
        self.model_name = model_name
        self._setup(device)

    def _setup(self, device):
        try:
            import torch
            import torchvision.models as models
            import torchvision.transforms as T

            self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")

            if self.model_name == "resnet50":
                backbone = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
                self.model = torch.nn.Sequential(*list(backbone.children())[:-1])  # Remove FC
                self.embed_dim = 2048
            elif self.model_name == "efficientnet_b0":
                backbone = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
                self.model = torch.nn.Sequential(*list(backbone.children())[:-1])
                self.embed_dim = 1280
            else:
                raise ValueError(f"Unknown model: {self.model_name}")

            self.model.eval().to(self.device)

            self.transform = T.Compose([
                T.Resize(256),
                T.CenterCrop(224),
                T.ToTensor(),
                T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ])
            self.backend = "pytorch"
            print(f"Loaded {self.model_name} (embed_dim={self.embed_dim})")

        except ImportError:
            self.backend = "hog"
            self.embed_dim = 8100
            print("PyTorch unavailable using HOG features (scikit-image)")

    def extract(self, image_path_or_array):
        """Extract embedding from image path or numpy array."""
        if self.backend == "pytorch":
            return self._extract_pytorch(image_path_or_array)
        return self._extract_hog(image_path_or_array)

    def _extract_pytorch(self, img_input):
        import torch
        from PIL import Image

        if isinstance(img_input, str):
            img = Image.open(img_input).convert("RGB")
        else:
            img = Image.fromarray(img_input)

        x = self.transform(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            feat = self.model(x)
        return feat.cpu().numpy().flatten()

    def _extract_hog(self, img_input):
        """HOG features as CNN fallback."""
        try:
            from skimage.feature import hog
            from skimage.transform import resize
            import cv2
        except ImportError:
            return np.random.rand(self.embed_dim)

        if isinstance(img_input, str):
            import cv2
            img = cv2.imread(img_input)
            if img is None:
                return np.zeros(self.embed_dim)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img = img_input

        img_resized = resize(img, (128, 128), anti_aliasing=True)
        feat = hog(img_resized, orientations=9, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), channel_axis=-1 if img_resized.ndim == 3 else None)
        self.embed_dim = len(feat)
        return feat


# ─── FAISS Index ──────────────────────────────────────────────────────────────

class SimilarityIndex:
    """L2 / cosine similarity index using FAISS or sklearn."""

    def __init__(self, embed_dim, metric="cosine"):
        self.embed_dim = embed_dim
        self.metric = metric
        self.image_paths = []
        self.embeddings = []
        self.backend = None
        self._build_index()

    def _build_index(self):
        try:
            import faiss
            if self.metric == "cosine":
                self.index = faiss.IndexFlatIP(self.embed_dim)  # Inner product (after L2 norm)
            else:
                self.index = faiss.IndexFlatL2(self.embed_dim)
            self.backend = "faiss"
            print("Using FAISS index")
        except ImportError:
            self.index = None
            self.backend = "sklearn"
            print("FAISS unavailable using sklearn NearestNeighbors")

    def add(self, path, embedding):
        """Add an image embedding to the index."""
        self.image_paths.append(path)
        self.embeddings.append(embedding.astype(np.float32))
        if self.backend == "faiss":
            vec = embedding.astype(np.float32).reshape(1, -1)
            if self.metric == "cosine":
                vec = vec / (np.linalg.norm(vec) + 1e-8)
            self.index.add(vec)

    def build_sklearn_index(self):
        """Build sklearn index after all embeddings are added."""
        if self.backend == "sklearn" and self.embeddings:
            from sklearn.neighbors import NearestNeighbors
            metric = "cosine" if self.metric == "cosine" else "euclidean"
            self.nn = NearestNeighbors(metric=metric, algorithm="brute")
            self.nn.fit(np.array(self.embeddings))

    def search(self, query_embedding, top_k=5):
        """Search for top_k most similar images."""
        query = query_embedding.astype(np.float32).reshape(1, -1)

        if self.backend == "faiss":
            if self.metric == "cosine":
                query = query / (np.linalg.norm(query) + 1e-8)
            distances, indices = self.index.search(query, top_k)
            return [(self.image_paths[i], float(distances[0][j]))
                    for j, i in enumerate(indices[0]) if i < len(self.image_paths)]

        elif self.backend == "sklearn":
            distances, indices = self.nn.kneighbors(query, n_neighbors=min(top_k, len(self.embeddings)))
            return [(self.image_paths[i], float(distances[0][j]))
                    for j, i in enumerate(indices[0])]

        return []

    def save(self, path="similarity_index.json"):
        data = {
            "paths": self.image_paths,
            "embeddings": [e.tolist() for e in self.embeddings],
            "embed_dim": self.embed_dim,
            "metric": self.metric,
        }
        with open(path, "w") as f:
            json.dump(data, f)
        print(f"Index saved to {path}")

    def load(self, path="similarity_index.json"):
        with open(path) as f:
            data = json.load(f)
        self.image_paths = data["paths"]
        self.embeddings = [np.array(e, dtype=np.float32) for e in data["embeddings"]]
        if self.backend == "faiss":
            for emb in self.embeddings:
                vec = emb.reshape(1, -1)
                if self.metric == "cosine":
                    vec = vec / (np.linalg.norm(vec) + 1e-8)
                self.index.add(vec)
        else:
            self.build_sklearn_index()
        print(f"Index loaded: {len(self.image_paths)} images")


# ─── Demo: Synthetic Image Gallery ────────────────────────────────────────────

def generate_synthetic_images(n=30, output_dir="synthetic_gallery"):
    """Generate colored pattern images for demo."""
    import cv2
    os.makedirs(output_dir, exist_ok=True)
    np.random.seed(42)
    paths = []

    for i in range(n):
        img = np.zeros((224, 224, 3), dtype=np.uint8)
        # Random pattern
        pattern = np.random.choice(["circle", "rect", "gradient"])
        color = tuple(np.random.randint(50, 255, 3).tolist())
        bg_color = tuple(np.random.randint(0, 100, 3).tolist())
        img[:] = bg_color

        if pattern == "circle":
            cv2.circle(img, (112, 112), np.random.randint(40, 100), color, -1)
        elif pattern == "rect":
            x1, y1 = np.random.randint(20, 80, 2)
            x2, y2 = x1 + np.random.randint(60, 120), y1 + np.random.randint(60, 120)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, -1)
        else:
            for j in range(224):
                frac = j / 224
                row_color = tuple(int(c * frac) for c in color)
                img[j, :] = row_color

        path = os.path.join(output_dir, f"img_{i:03d}_{pattern}.jpg")
        cv2.imwrite(path, img)
        paths.append(path)

    print(f"Generated {n} synthetic images in {output_dir}/")
    return paths


def visualize_results(query_path, results, n_cols=5):
    """Visualize query and top-K similar images."""
    import cv2

    def load_rgb(p):
        img = cv2.imread(p)
        if img is None:
            return np.zeros((224, 224, 3), dtype=np.uint8)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    n_show = min(len(results) + 1, n_cols + 1)
    fig, axes = plt.subplots(1, n_show, figsize=(3 * n_show, 3.5))
    if n_show == 1:
        axes = [axes]

    # Query image
    axes[0].imshow(load_rgb(query_path))
    axes[0].set_title("QUERY", fontsize=10, color="red", fontweight="bold")
    axes[0].axis("off")

    # Results
    for i, (path, score) in enumerate(results[:n_cols]):
        axes[i + 1].imshow(load_rgb(path))
        title = f"#{i+1}\n{score:.3f}\n{Path(path).stem}"
        axes[i + 1].set_title(title, fontsize=7)
        axes[i + 1].axis("off")

    plt.suptitle(f"Top-{len(results)} Similar Images", fontsize=13)
    plt.tight_layout()
    plt.savefig("similarity_results.png", dpi=100)
    print("Results saved to similarity_results.png")
    plt.close()


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gallery", default="synthetic_gallery",
                        help="Directory of images to index")
    parser.add_argument("--query", default=None, help="Query image path")
    parser.add_argument("--model", default="resnet50")
    parser.add_argument("--top_k", type=int, default=5)
    args = parser.parse_args()

    print("=" * 55)
    print("  IMAGE SIMILARITY SEARCH ENGINE")
    print("=" * 55)

    # Generate demo images if gallery doesn't exist
    if not os.path.isdir(args.gallery) or len(list(Path(args.gallery).glob("*.jpg"))) < 5:
        image_paths = generate_synthetic_images(n=30, output_dir=args.gallery)
    else:
        image_paths = list(map(str, Path(args.gallery).glob("*.jpg")))
        print(f"Found {len(image_paths)} images in {args.gallery}")

    # Extractor
    print(f"\n[1] Loading feature extractor ({args.model})...")
    extractor = FeatureExtractor(model_name=args.model)

    # Build index
    print(f"\n[2] Indexing {len(image_paths)} images...")
    index = SimilarityIndex(embed_dim=extractor.embed_dim, metric="cosine")
    t0 = time.time()
    for i, path in enumerate(image_paths):
        emb = extractor.extract(path)
        index.add(path, emb)
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{len(image_paths)} indexed...")
    if index.backend == "sklearn":
        index.build_sklearn_index()
    print(f"Indexing done in {time.time()-t0:.2f}s")

    # Save index
    index.save("image_index.json")

    # Query
    query_path = args.query or image_paths[0]
    print(f"\n[3] Querying: {query_path}")
    query_emb = extractor.extract(query_path)
    results = index.search(query_emb, top_k=args.top_k + 1)  # +1 because query itself may match
    # Remove query itself if it appears
    results = [(p, s) for p, s in results if p != query_path][:args.top_k]

    print(f"\nTop {len(results)} similar images:")
    for i, (path, score) in enumerate(results, 1):
        print(f"  {i}. {os.path.basename(path)} (score={score:.4f})")

    # Visualize
    print("\n[4] Visualizing results...")
    visualize_results(query_path, results)

    print("\nDone!")
