"""
Production-grade sentiment classifier.
Baseline: TF-IDF + LogisticRegression
Advanced: fine-tuned DistilBERT (if transformers available)
"""

import logging
import os
import pickle
import random
import shutil
import sys
import tarfile
import time
import urllib.request
from typing import Dict, List, Optional, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

BASELINE_PATH = os.path.join(MODEL_DIR, "baseline.pkl")
BERT_PATH     = os.path.join(MODEL_DIR, "bert_model")
LABELS        = {0: "negative", 1: "positive"}

# Real sentiment data: the Cornell "sentence polarity dataset v1.0" (Pang & Lee, 2005),
# 5,331 positive + 5,331 negative movie-review snippets from Rotten Tomatoes. It is the
# same data as the Hugging Face "rotten_tomatoes" dataset. ~0.5 MB, downloaded once.
DATA_DIR      = "data"
POLARITY_URL  = "https://www.cs.cornell.edu/people/pabo/movie-review-data/rt-polaritydata.tar.gz"
POLARITY_TGZ  = os.path.join(DATA_DIR, "rt-polaritydata.tar.gz")


def _download_polarity(retries: int = 5) -> None:
    """Download the dataset once. Writes to a temporary file and renames it only when
    complete, so an interrupted download never leaves a broken archive behind."""
    if os.path.exists(POLARITY_TGZ):
        return
    os.makedirs(DATA_DIR, exist_ok=True)
    tmp = POLARITY_TGZ + ".part"
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Downloading sentiment dataset from {POLARITY_URL} (attempt {attempt}) ...")
            # timeout: a stalled connection raises an error (and is retried) instead of hanging
            with urllib.request.urlopen(POLARITY_URL, timeout=30) as resp, open(tmp, "wb") as f:
                shutil.copyfileobj(resp, f)
            with tarfile.open(tmp, "r:gz") as tar:  # make sure the archive is complete
                tar.getmembers()
            os.replace(tmp, POLARITY_TGZ)
            return
        except Exception as e:
            logger.warning(f"Download failed: {e}")
            if os.path.exists(tmp):
                os.remove(tmp)
            time.sleep(2 * attempt)
    raise RuntimeError(f"Could not download {POLARITY_URL}. Check your internet connection, "
                       f"or download it manually into {DATA_DIR}/")


def _make_sentiment_data(n: Optional[int] = None, seed: int = 42) -> Tuple[List[str], List[int]]:
    """Load a balanced, labelled sentiment dataset (1 = positive, 0 = negative).

    n = total number of examples to return (half positive, half negative); None = all 10,662.
    """
    _download_polarity()
    with tarfile.open(POLARITY_TGZ, "r:gz") as tar:
        def read(name):
            member = next(m for m in tar.getmembers() if m.name.endswith(name))
            return [l.strip() for l in tar.extractfile(member).read().decode("latin-1").splitlines() if l.strip()]
        pos, neg = read("rt-polarity.pos"), read("rt-polarity.neg")
    rng = random.Random(seed)
    rng.shuffle(pos); rng.shuffle(neg)
    if n is not None:
        pos, neg = pos[:n//2], neg[:n//2]
    texts  = pos + neg
    labels = [1] * len(pos) + [0] * len(neg)
    return texts, labels


def train_baseline() -> Dict:
    logger.info("Training TF-IDF + Logistic Regression baseline...")
    texts, labels = _make_sentiment_data()  # all 10,662 snippets
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=20000, ngram_range=(1, 2), sublinear_tf=True)),
        ("clf",   LogisticRegression(max_iter=1000, C=1.0)),
    ])
    t0 = time.time()
    pipeline.fit(X_train, y_train)
    train_time = time.time() - t0

    preds = pipeline.predict(X_test)
    report = classification_report(y_test, preds, output_dict=True)

    with open(BASELINE_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    logger.info(f"Baseline accuracy: {report['accuracy']:.4f} (trained in {train_time:.1f}s)")
    return {"model": "baseline", "accuracy": report["accuracy"], "report": report}


def train_bert(epochs: int = 2, n_samples: int = 1000) -> Dict:
    """Fine-tune DistilBERT for sentiment classification (needs torch + accelerate).

    Downloads distilbert-base-uncased (~270 MB) on first use. On CPU, keep n_samples small.
    """
    try:
        from transformers import (AutoModelForSequenceClassification,
                                   AutoTokenizer, Trainer, TrainingArguments)
        import torch
        from torch.utils.data import Dataset

        class SentDataset(Dataset):
            def __init__(self, texts, labels, tok, max_len=128):
                self.enc    = tok(texts, truncation=True, padding=True, max_length=max_len, return_tensors="pt")
                self.labels = torch.tensor(labels)
            def __len__(self): return len(self.labels)
            def __getitem__(self, i):
                return {k: v[i] for k, v in self.enc.items()} | {"labels": self.labels[i]}

        texts, labels = _make_sentiment_data(n_samples)
        X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

        tok   = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

        args = TrainingArguments(
            output_dir=BERT_PATH, num_train_epochs=epochs,
            per_device_train_batch_size=16, per_device_eval_batch_size=32,
            logging_steps=50, eval_strategy="epoch",
            save_strategy="epoch",          # must match eval_strategy for load_best_model_at_end
            save_total_limit=1,             # keep disk use small (checkpoints are large)
            load_best_model_at_end=True,
        )
        trainer = Trainer(
            model=model, args=args,
            train_dataset=SentDataset(X_train, y_train, tok),
            eval_dataset=SentDataset(X_test, y_test, tok),
        )
        trainer.train()
        trainer.save_model(BERT_PATH)
        tok.save_pretrained(BERT_PATH)
        logger.info(f"DistilBERT saved to {BERT_PATH}")
        return {"model": "bert", "status": "trained"}
    except ImportError as e:
        logger.warning(f"Skipping BERT training: {e}")
        return {"model": "bert", "status": "skipped", "reason": f"missing library: {e}"}


_baseline_model = None
_bert_model     = None
_bert_tokenizer = None


def load_baseline():
    global _baseline_model
    if _baseline_model is None:
        with open(BASELINE_PATH, "rb") as f:
            _baseline_model = pickle.load(f)
    return _baseline_model


def load_bert():
    global _bert_model, _bert_tokenizer
    if _bert_model is None:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        import torch
        _bert_tokenizer = AutoTokenizer.from_pretrained(BERT_PATH)
        _bert_model     = AutoModelForSequenceClassification.from_pretrained(BERT_PATH)
        _bert_model.eval()
    return _bert_model, _bert_tokenizer


def predict_baseline(text: str) -> Dict:
    t0 = time.time()
    m  = load_baseline()
    p  = m.predict([text])[0]
    pr = m.predict_proba([text])[0]
    return {"label": LABELS[p], "confidence": round(float(max(pr)) * 100, 2),
            "model_version": "baseline", "inference_ms": round((time.time()-t0)*1000, 2)}


def predict_bert(text: str) -> Dict:
    import torch
    t0 = time.time()
    model, tok = load_bert()
    inputs = tok(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.softmax(logits, dim=1)[0].tolist()
    p = int(torch.argmax(logits))
    return {"label": LABELS[p], "confidence": round(max(probs) * 100, 2),
            "model_version": "bert", "inference_ms": round((time.time()-t0)*1000, 2)}


def predict(text: str, model_version: str = "baseline") -> Dict:
    if model_version == "bert" and os.path.exists(BERT_PATH):
        try:
            return predict_bert(text)
        except Exception:
            pass
    return predict_baseline(text)


if __name__ == "__main__":
    train_baseline()
    print("\nTest prediction:", predict("This is absolutely amazing and wonderful!"))
    print("Test prediction:", predict("This is terrible and I hate it."))
    if "--bert" in sys.argv:  # optional and slow on CPU: python main.py --bert
        print(train_bert())
        print("BERT prediction:", predict("This is terrible and I hate it.", "bert"))
