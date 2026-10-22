# Project 06: Production Model (MLOps)

This project wraps a simple **sentiment classifier** (it labels text as `positive` or `negative`) in the extra machinery a real service needs: input checks, **rate limiting** (a cap on how many requests one user can make per minute), request logging, **metrics** (numbers about the service, such as how many predictions it made and how fast), a basic **drift** check (a warning when the model seems less sure than usual, which can mean incoming data has changed), a **health endpoint**, and a **Docker** setup (Docker packages the app and everything it needs into a "container" that runs the same way on any machine).

The model is trained on real sentiment data: the Cornell **sentence polarity dataset** (5,331 positive and 5,331 negative movie-review snippets from Rotten Tomatoes, the same data as the Hugging Face `rotten_tomatoes` dataset).

| | |
|---|---|
| **What you will learn** | Training and saving a scikit-learn pipeline; serving it with FastAPI; Pydantic validation; rate limiting with `slowapi`; Prometheus-style metrics; a simple drift check; health checks; optional DistilBERT fine-tuning; reading a multi-stage Dockerfile and a docker-compose stack (app + Prometheus + Grafana) |
| **Difficulty** | Intermediate |
| **Time needed** | About 1 hour without Docker; add 1-2 hours for the Docker route and exercises |
| **Runs on** | CPU, no API key. Needs internet once, to download the 0.5 MB dataset (and about 270 MB more if you fine-tune DistilBERT) |

---

## 1. What is in this folder

| File | What it does |
|---|---|
| `main.py` | Downloads the sentiment dataset into `data/` (once), trains **TF-IDF + Logistic Regression** (the "baseline"), saves it to `models/baseline.pkl`, and provides `predict()`. `train_bert()` optionally fine-tunes DistilBERT into `models/bert_model/` |
| `api.py` | FastAPI service: `POST /predict`, `POST /predict/batch`, `GET /health`, `GET /model-info`, `GET /metrics` (JSON summary), `GET /metrics/prometheus` (Prometheus text format), `GET /` (web page). Adds a rate limit and a request-logging middleware |
| `monitoring.py` | Keeps the last 1000 predictions in memory (with the same `request_id` the client received), updates Prometheus counters, histograms and gauges, builds the metrics summary, and runs the drift check (warns if average confidence over the last 100 predictions is below 70%) |
| `templates/index.html` | Web page with three tabs: Single Predict, Batch Mode, Metrics |
| `Dockerfile` | Multi-stage build on `python:3.11-slim`, non-root user, **trains the baseline during the build** so the image ships a model, health check, one uvicorn worker on port 8005 |
| `docker-compose.yml` | Runs the app together with Prometheus and Grafana |
| `prometheus.yml` | Tells Prometheus to scrape `app:8005/metrics/prometheus` every 15 seconds |
| `.dockerignore` | Keeps `.venv/`, `models/`, `data/` and caches out of the Docker image |
| `requirements.txt` | Pinned libraries (FastAPI, scikit-learn, slowapi, prometheus-client, transformers, accelerate, torch, ...) |
| `notes/06_production_model.md` | Longer explanation of the concepts |

---

## 2. Before you start (prerequisites)

**Notebooks to finish first** (paths are relative to this folder):

- Text classification: [`../../07_NLP/03_text_classification.ipynb`](../../07_NLP/03_text_classification.ipynb)
- Serving models: [`../../12_FastAPI/01_fastapi_intro.ipynb`](../../12_FastAPI/01_fastapi_intro.ipynb), [`../../12_FastAPI/03_ml_serving_with_fastapi.ipynb`](../../12_FastAPI/03_ml_serving_with_fastapi.ipynb), [`../../12_FastAPI/04_industry_production_ml_api.ipynb`](../../12_FastAPI/04_industry_production_ml_api.ipynb)
- Monitoring: [`../../15_MLOps/06_monitoring/01_monitoring.ipynb`](../../15_MLOps/06_monitoring/01_monitoring.ipynb)
- Docker (for the Docker route): [`../../17_Docker/01_docker_basics.ipynb`](../../17_Docker/01_docker_basics.ipynb), [`../../17_Docker/02_docker_for_ml.ipynb`](../../17_Docker/02_docker_for_ml.ipynb)

**Python version:** 3.10, 3.11 or 3.12. `pip install --dry-run -r requirements.txt` resolves with no conflicts on Python 3.12. Python 3.13+ won't work with these pins (`numpy==1.26.4`, `torch==2.4.1`). The Dockerfile uses Python 3.11.

**API keys:** none. **Docker (optional):** Docker Desktop (Windows/Mac) or Docker Engine with the Compose plugin (Linux).

---

## 3. Run it without Docker

Run every command from inside this folder (`21_Projects/06_production_model`). The code uses relative paths (`data/`, `models/`, `templates/index.html`).

### Step 1: Create and activate a virtual environment

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 2: Install the libraries

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

💡 **Tip (Linux, CPU only):** `torch==2.4.1` from PyPI on Linux also downloads several GB of CUDA packages. Torch is only needed for the optional DistilBERT step. The CPU build is much smaller:

```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
```

### Step 3: Train the baseline model

```bash
python main.py
```

Output I got (about 8 seconds once the dataset was downloaded):

```
INFO:__main__:Baseline accuracy: 0.7745 (trained in 2.9s)

Test prediction: {'label': 'positive', 'confidence': 83.15, 'model_version': 'baseline', 'inference_ms': 53.63}
Test prediction: {'label': 'negative', 'confidence': 51.46, 'model_version': 'baseline', 'inference_ms': 7.75}
```

The two test sentences are "This is absolutely amazing and wonderful!" and "This is terrible and I hate it.". About 77% accuracy is typical for a bag-of-words model on these short, tricky movie-review snippets. Note how unsure (51%) it is about the second sentence; see Known issues.

The dataset is downloaded once into `data/rt-polaritydata.tar.gz`, with retries if the connection drops.

### Step 4 (optional, slow): fine-tune DistilBERT

```bash
python main.py --bert          # baseline + DistilBERT (1000 samples, 2 epochs)
```

This downloads `distilbert-base-uncased` (about 270 MB) the first time, and needs `torch` and `accelerate` (both in `requirements.txt`). On a CPU it is slow. I verified the pipeline with a small run:

```bash
python -c "import main; print(main.train_bert(epochs=1, n_samples=200))"
# ... {'train_runtime': '305.4', 'train_loss': '0.6921', 'epoch': '1'}
# {'model': 'bert', 'status': 'trained'}
```

200 samples for one epoch is far too little to learn anything (its predictions were all about 50-53% confident), but it showed that training, saving and serving with `model_version: "bert"` all work. The full `--bert` run was **not** completed here; at the observed speed (about 30-40 seconds per step on a busy 8-core CPU, 100 steps) expect roughly an hour. The saved folder `models/bert_model/` was about 1 GB, including one checkpoint.

### Step 5: Start the API

```bash
python api.py
```

This starts on **port 8005**. To pick another port:

```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

The examples below use port 8000. Open <http://127.0.0.1:8000/> for the web page, or <http://127.0.0.1:8000/docs> for FastAPI's interactive docs.

### Step 6: Try it with curl

On Windows PowerShell use `curl.exe`, and for JSON bodies use a file: `-d @body.json`.

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok","model_loaded":true}
```

Before training, I got `{"status":"degraded","model_loaded":false}`. Both `/predict` and `/predict/batch` then return HTTP 503 `{"detail":"Model not found run python main.py to train first"}`.

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" \
     -d '{"text":"It was boring and far too long"}'
```
```json
{"request_id":"e9fcc56f","text_preview":"It was boring and far too long","label":"negative","confidence":94.56,"model_version":"baseline","inference_ms":8.96}
```

More results I got:

| Text | Label | Confidence |
|---|---|---|
| A beautiful, moving story | positive | 88.3% |
| Worst purchase ever, a complete waste of money | negative | 86.0% |
| This movie was absolutely wonderful, I loved it | positive | 54.5% |
| The food was delicious and the staff were friendly | **negative** (wrong) | 64.3% |

Batch prediction (1-50 texts; each item gets its own `request_id`):

```bash
curl -X POST http://127.0.0.1:8000/predict/batch -H "Content-Type: application/json" \
     -d '{"texts":["I love it","I hate it"]}'
```
```json
{"count":2,"results":[{"request_id":"d98d7f86","text_preview":"I love it","label":"positive","confidence":58.19,...},{"request_id":"f16f0a42","text_preview":"I hate it","label":"positive","confidence":50.31,...}]}
```

Validation (HTTP 422): an empty `text`, an empty string inside `texts`, an empty `texts` list, or any `model_version` other than `baseline`/`bert` is rejected. For example:

```
{"detail":[{"type":"string_pattern_mismatch","loc":["body","model_version"],"msg":"String should match pattern '^(baseline|bert)$'",...}]}
```

Metrics. The `request_id`s in `recent` are the same ones the clients received:

```bash
curl http://127.0.0.1:8000/metrics
curl http://127.0.0.1:8000/metrics/prometheus
```
```
predictions_total{label="positive",model="baseline"} 4.0
predictions_total{label="negative",model="baseline"} 58.0
prediction_latency_ms_count{model="baseline"} 62.0
avg_confidence{model="baseline"} 55.43
```

Rate limit: `/predict` allows 60 requests per minute per client IP. In a loop of 60 extra requests I got 54 × `200` and then 6 × `429` `{"detail":"60 per 1 minute"}`.

Drift: after that loop of 60 × `"hello"` (a neutral word, about 55% confidence), `/metrics` reported `"drift_detected": true, "avg_confidence": 55.43, "recommendation": "Consider retraining"`. Text unlike the training data lowers the confidence, which is exactly what the check is meant to notice.

Stop the server with `Ctrl+C`.

**How this was verified:** I ran it on Python 3.12, using newer library versions than the pins (FastAPI 0.138, scikit-learn 1.9, transformers 5.12, accelerate 1.14, slowapi 0.1.9, prometheus-client 0.21.0). The pins themselves were checked with `pip install --dry-run` only.

---

## 4. Run it with Docker (NOT verified: read from the files only)

> No Docker command was run while writing this. `docker-compose.yml` and `prometheus.yml` were checked only for valid YAML with Python.

**App container only:**

```bash
docker build -t sentiment-api .        # also trains the baseline (needs internet during the build)
docker run --name sentiment -p 8005:8005 sentiment-api
curl http://localhost:8005/health      # expected: {"status":"ok","model_loaded":true}
```

**Full stack (app + Prometheus + Grafana):**

```bash
docker compose up --build -d
```

- App: <http://localhost:8005>
- Prometheus: <http://localhost:9090>. Its `prometheus.yml` scrapes `app:8005/metrics/prometheus`; check **Status → Targets**.
- Grafana: <http://localhost:3000>, login `admin` / `admin`. Add a Prometheus data source with URL `http://prometheus:9090` (none is set up automatically).

Stop with `docker compose down`. The `model-store` volume holds `/app/models`. On the first start it is filled from the image, but after you rebuild the image it keeps the *old* model, so use `docker compose down -v` to reset it. To fine-tune BERT inside the container: `docker compose exec app python -c "import main; print(main.train_bert(epochs=1, n_samples=200))"`.

---

## 5. How it works

```
 client ──► POST /predict {"text": "...", "model_version": "baseline"}
              │
              ▼
   log_requests middleware (prints method, path, status, ms)
              │
   Pydantic validation (1-10000 chars, version baseline|bert) ─► 422
              │
   slowapi limiter (60/min /predict, 20/min /batch per IP) ───► 429
              │
              ▼
   main.predict(text, version)
     ├─ "bert" and models/bert_model exists → DistilBERT (any error → baseline)
     └─ baseline: models/baseline.pkl  (TF-IDF → LogisticRegression)   missing → 503
              │
              ▼
   result {label, confidence, model_version, inference_ms}
              ├──► returned to the client with request_id + text_preview
              └──► monitoring.log_prediction(text, result, request_id)
                     ├─ in-memory deque (last 1000) ──► GET /metrics (JSON + drift)
                     └─ Prometheus Counter/Histogram/Gauge ──► GET /metrics/prometheus
                                                                   │
                         (docker-compose) Prometheus scrapes every 15 s ─► Grafana
```

---

## 6. Known issues and limitations

- **The baseline is small and was trained on movie reviews.** It is good at review-style text ("boring and far too long" → negative, 94.6%) but weak on short everyday sentences: "The food was delicious and the staff were friendly" → negative, "I hate it" → positive at 50.3%. A bag-of-words model can't read context. DistilBERT (Step 4, trained properly) is the upgrade path; so is adding your own domain's labelled examples.
- **Metrics, logs and rate-limit counters live in process memory.** The Dockerfile therefore runs one worker. With `--workers 2` (tested earlier), each worker kept its own numbers: `/metrics` showed only part of the traffic, and the rate limit effectively doubled. Scaling out needs shared storage (Prometheus multiprocess mode, a Redis-backed limiter).
- **The drift check is a fixed 70% rule.** Neutral or off-topic text (like "hello") pushes the average below it. A better rule compares with the confidence measured on the test set.
- **Full DistilBERT fine-tuning was not run to completion** (only the 200-sample check), and it is slow on CPU.
- **Docker and Compose were not run** (section 4 is from reading the files). Two things to know: `prom/prometheus:latest` and `grafana/grafana:latest` are unpinned image tags, and a plain Linux build installs CUDA-enabled torch (large image). Add `--extra-index-url https://download.pytorch.org/whl/cpu` to the Dockerfile's `pip install` line if size matters.
- **Small things:** `/health` returns HTTP 200 even when "degraded"; the Batch tab inserts your text into the page without HTML-escaping it; the first BERT prediction is slow because the model is loaded on first use.

---

## 7. Ideas to extend it

1. **Easy: test the model honestly.** Write 20 everyday sentences of your own with labels, and measure the baseline's accuracy on them. Compare with the 77% test accuracy and explain the difference.
2. **Easy-medium: a better drift rule.** Save the average confidence on the test set next to the model during training, and flag drift when live confidence drops well below *that* value.
3. **Medium: train DistilBERT properly.** Run `python main.py --bert` (or more samples and epochs) on a machine with time or a GPU, then compare baseline vs BERT on your 20 sentences.
4. **Medium: shared rate limiting.** Add a Redis service to the compose file, point slowapi at it (`Limiter(..., storage_uri="redis://redis:6379")`), and confirm the limit stays at 60 per minute with 2 workers.
5. **Harder: model versioning.** Save models as `models/baseline_v1.pkl`, `..._v2.pkl`, and add `POST /reload` plus a `version` field in `/health`, so you can roll out a new model without restarting the server.
