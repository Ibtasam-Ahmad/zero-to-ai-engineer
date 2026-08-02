"""
Sentiment Analysis API Fine-tuned DistilBERT on SST-2
Requirements: transformers datasets torch fastapi uvicorn jinja2
"""

import os
from contextlib import asynccontextmanager
from typing import List

import torch
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    pipeline,
)

# ── Config ────────────────────────────────────────────────────────────────────
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"  # pretrained baseline
DEVICE = 0 if torch.cuda.is_available() else -1

# ── Schemas ───────────────────────────────────────────────────────────────────
class TextInput(BaseModel):
    text: str

class BatchInput(BaseModel):
    texts: List[str]

class SentimentResult(BaseModel):
    text: str
    label: str
    confidence: float

# ── Lifespan: load model once at startup ─────────────────────────────────────
classifier = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global classifier
    print(f"Loading model: {MODEL_NAME}")
    classifier = pipeline("sentiment-analysis", model=MODEL_NAME, device=DEVICE)
    print("Model ready.")
    yield
    classifier = None

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Sentiment Analyzer", lifespan=lifespan)

HTML_FRONTEND = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sentiment Analyzer</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body { background: #0f0f1a; color: #e0e0e0; }
    .card { background: #1a1a2e; border: 1px solid #333; }
    .positive { color: #4ade80; }
    .negative { color: #f87171; }
    .confidence-bar { height: 8px; border-radius: 4px; }
  </style>
</head>
<body>
<div class="container py-5">
  <h1 class="text-center mb-4">🧠 Sentiment Analyzer</h1>
  <div class="card p-4 mb-4">
    <div class="mb-3">
      <textarea id="inputText" class="form-control bg-dark text-light border-secondary"
        rows="4" placeholder="Enter text to analyze..."></textarea>
    </div>
    <button onclick="analyze()" class="btn btn-primary w-100">Analyze Sentiment</button>
  </div>
  <div id="result" class="card p-4" style="display:none">
    <h5>Result</h5>
    <div id="label" class="fs-3 fw-bold mb-2"></div>
    <div class="mb-1 text-muted">Confidence</div>
    <div class="progress mb-2" style="height:8px">
      <div id="bar" class="progress-bar confidence-bar" role="progressbar"></div>
    </div>
    <div id="confText" class="text-muted small"></div>
  </div>
</div>
<script>
async function analyze() {
  const text = document.getElementById("inputText").value.trim();
  if (!text) return;
  const res = await fetch("/analyze", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({text})
  });
  const data = await res.json();
  document.getElementById("result").style.display = "block";
  const labelEl = document.getElementById("label");
  labelEl.textContent = data.label === "POSITIVE" ? "😊 POSITIVE" : "😞 NEGATIVE";
  labelEl.className = "fs-3 fw-bold mb-2 " + (data.label === "POSITIVE" ? "positive" : "negative");
  const pct = (data.confidence * 100).toFixed(1);
  const bar = document.getElementById("bar");
  bar.style.width = pct + "%";
  bar.className = "progress-bar confidence-bar " + (data.label === "POSITIVE" ? "bg-success" : "bg-danger");
  document.getElementById("confText").textContent = `Confidence: ${pct}%`;
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def frontend():
    return HTML_FRONTEND

@app.post("/analyze", response_model=SentimentResult)
def analyze(body: TextInput):
    result = classifier(body.text[:512])[0]
    return SentimentResult(
        text=body.text,
        label=result["label"],
        confidence=round(result["score"], 4),
    )

@app.post("/analyze/batch", response_model=List[SentimentResult])
def analyze_batch(body: BatchInput):
    truncated = [t[:512] for t in body.texts]
    results = classifier(truncated)
    return [
        SentimentResult(text=t, label=r["label"], confidence=round(r["score"], 4))
        for t, r in zip(body.texts, results)
    ]

# ── Optional: fine-tune on SST-2 ─────────────────────────────────────────────
def finetune(output_dir: str = "./finetuned-sentiment", epochs: int = 1):
    """Fine-tune DistilBERT on SST-2 (run this separately before serving)."""
    from datasets import load_dataset

    print("Loading SST-2 dataset...")
    dataset = load_dataset("glue", "sst2")
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    def tokenize(batch):
        return tokenizer(batch["sentence"], truncation=True, padding="max_length", max_length=128)

    dataset = dataset.map(tokenize, batched=True)
    dataset = dataset.rename_column("label", "labels")
    dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

    model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=32,
        per_device_eval_batch_size=64,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        logging_steps=100,
        fp16=torch.cuda.is_available(),
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["validation"],
    )
    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--finetune", action="store_true", help="Fine-tune before serving")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.finetune:
        finetune()
        MODEL_NAME = "./finetuned-sentiment"

    print(f"Starting server at http://{args.host}:{args.port}")
    uvicorn.run("01_sentiment_analyzer:app", host=args.host, port=args.port, reload=False)
