# 06 Production Model: From Prototype to Operations

This project takes a model the rest of the curriculum would be content to simply train and serve, and asks the harder question: *what does it take to run this thing reliably in the real world?* The model itself a **sentiment classifier** that labels a piece of text as positive or negative is intentionally modest. The point of the project is everything *around* the model: the operational machinery that distinguishes a prototype from a **production** system. This is the domain of **MLOps** (Machine Learning Operations), the engineering discipline of deploying, serving, monitoring, and maintaining models under real traffic.

## What It Does

At its core, the service classifies the sentiment of input text. But it does so with the full apparatus of a production deployment: it offers two models at different cost/quality trade-offs, protects itself against abuse, records every prediction, exposes operational metrics, watches for the model silently degrading over time, reports its own health, and ships as a self-contained, reproducible container alongside a supporting infrastructure stack.

## The Two-Model Strategy

The classifier comes in two versions, illustrating a common production trade-off between speed and sophistication.

- The **baseline** is a **TF-IDF + Logistic Regression** pipeline. *TF-IDF* (Term Frequency-Inverse Document Frequency) turns text into numbers by weighting words by how distinctive they are, and logistic regression draws a decision boundary over those numbers. It is fast, tiny, cheap to run, and trains in seconds the dependable default.
- The **advanced** model is a **fine-tuned DistilBERT**. DistilBERT is a compact **transformer** language model; *fine-tuning* adapts a pre-trained model to this specific sentiment task. It is more accurate but heavier and slower.

The serving logic lets a request choose its model version and falls back to the baseline if the advanced model isn't trained or available. Offering tiered models a fast default and a premium option is a frequent production pattern, letting callers pick the right point on the cost/quality curve.

## Architecture and Components

### Model training and inference (`main.py`)

Builds a labelled sentiment dataset (the Cornell *sentence polarity* dataset: 5,331 positive and 5,331 negative movie-review snippets from Rotten Tomatoes, the same data as the Hugging Face `rotten_tomatoes` dataset, downloaded once into `data/`), trains the baseline pipeline and (optionally) fine-tunes DistilBERT, persists both to disk, and provides a unified `predict` function. Importantly, every prediction returns not just a label and **confidence** but also the **inference latency** in milliseconds and the model version used operational facts that the monitoring layer depends on.

### The production API (`api.py`)

A FastAPI service that wraps the model with several production-grade concerns layered on top of plain serving:

- **Input validation** via Pydantic, enforcing length limits on text and restricting the model-version field to known values, rejecting malformed or oversized requests up front.
- **Rate limiting** via `slowapi`, capping how many requests a single client may make per minute. This protects the service from being overwhelmed accidentally or maliciously and is essential when an endpoint is exposed to the open internet.
- **Request logging middleware** that records the method, path, status, and duration of every request, giving a continuous trace of traffic.
- **Batch prediction** (`/predict/batch`) for classifying many texts in one call, more efficient than many separate requests.
- **A health endpoint** that reports `ok` or `degraded` depending on whether the model loaded the signal orchestration systems use to route traffic only to healthy instances.
- **Metrics endpoints** exposing both a human-readable summary and a machine-readable **Prometheus** feed (described below).

### Monitoring and observability (`monitoring.py`)

This is the project's distinguishing piece. A model that works on day one can quietly rot as the world changes; *observability* is how you notice. The module provides:

- **Prediction logging** every prediction is recorded in a rolling in-memory buffer with its label, confidence, latency, and model version.
- **Prometheus metrics** the service publishes counters (total predictions by model and label), histograms (latency distribution), and gauges (rolling average confidence) in the format **Prometheus**, an industry-standard metrics system, knows how to scrape. These feed dashboards and alerts.
- **A metrics summary** aggregate statistics like positive/negative rates, average latency, and average confidence over recent traffic.
- **Drift detection** a simple stub that watches the rolling average confidence and flags **drift** when it falls below a threshold, recommending retraining. *Model drift* is the gradual degradation that occurs when live data diverges from the data a model was trained on; catching it early is a core MLOps responsibility. Falling confidence is one cheap early-warning signal.

### Containerization and deployment (`Dockerfile`, `docker-compose.yml`)

The final layer makes the whole thing portable and reproducible. The **Dockerfile** packages the application into a **container** a self-contained image bundling the code, dependencies, and runtime so it runs identically anywhere. It demonstrates several best practices: a **multi-stage build** (compiling dependencies in one stage and copying only the results into a lean final image), running as a **non-root user** for security, a built-in container **health check**, and training the baseline model during the build so the image ships ready to serve. It launches a single worker process on purpose: the metrics, prediction log and rate-limit counters live in process memory, so several workers would each keep their own partial numbers (scaling out properly needs shared storage, such as Prometheus multiprocess mode or a Redis-backed rate limiter).

The **docker-compose.yml** file goes further, defining the *full operational stack* as a set of cooperating services orchestrated together:

- the **app** itself,
- **Prometheus**, scraping and storing the app's metrics,
- **Grafana**, a dashboarding tool for visualizing those metrics,

all wired together with persistent volumes, restart policies, and health checks. Prometheus reads its scrape settings from `prometheus.yml`, which points it at the app's `/metrics/prometheus` endpoint. This mirrors how a real deployment composes an application with its monitoring and supporting infrastructure rather than running a model in isolation.

### The web interface (`templates/index.html`)

A page for submitting text, choosing a model, and viewing the classification along with operational details.

## Data Flow, End to End

```
client request
        │
        ▼
rate limiter  →  Pydantic validation  →  request-logging middleware
        │
        ▼
predict(text, model_version)  →  baseline (TF-IDF + LogReg)  or  DistilBERT
        │                                   │
        ▼                                   ▼
result {label, confidence, latency, version}
        │
        ├──►  returned to client
        └──►  monitoring.log_prediction()  →  rolling log + Prometheus counters/histograms/gauges
                                                        │
                                                        ▼
                                   /metrics summary + /metrics/prometheus + drift check
                                                        │
                                                        ▼
        Prometheus scrapes  →  Grafana dashboards   (all defined in docker-compose)
```

The production architecture, with the hardened API path, the monitoring side-channel, and the Docker Compose stack:

```mermaid
flowchart TD
    A[Client request] --> B[Rate limiter slowapi]
    B --> C[Pydantic validation]
    C --> D[Request-logging middleware]
    D --> E[predict text, model_version]
    E --> F[Baseline TF-IDF plus LogReg]
    E --> G[DistilBERT advanced]
    F --> H[Result: label, confidence, latency, version]
    G --> H
    H --> I[Returned to client]
    H --> J[monitoring.log_prediction]
    J --> K[Rolling log plus Prometheus counters, histograms, gauges]
    K --> L[/metrics summary, /metrics/prometheus, drift check]
    subgraph Stack [docker-compose stack]
        M[App]
        L --> O[Prometheus scrapes]
        O --> P[Grafana dashboards]
    end
    L --> M
```

## Concepts Demonstrated

- **MLOps** the operational discipline of running models in production, not just training them.
- **Tiered model serving** a fast baseline and a heavier, more accurate model, selectable per request with fallback.
- **API hardening** input validation, rate limiting, and request logging to make a service robust against real traffic.
- **Observability** prediction logging, Prometheus metrics (counters, histograms, gauges), and human-readable summaries.
- **Model drift detection** monitoring for silent degradation and signaling when retraining is warranted.
- **Health checks** exposing readiness so orchestrators route traffic only to healthy instances.
- **Containerization with Docker** multi-stage builds, non-root execution, and reproducible images.
- **Multi-service orchestration with Docker Compose** composing the app with Prometheus and Grafana into a complete deployable stack.

This project is the natural endpoint of the collection. It returns to the simplest kind of model a text classifier precisely so the spotlight can fall on everything that surrounds a model once it has to *stay running*: the difference between a model that works and a system you can trust.
