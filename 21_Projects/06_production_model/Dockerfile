# Multi-stage Dockerfile for production sentiment API

# ── Stage 1: builder ──────────────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: production ───────────────────────────────────────
FROM python:3.11-slim AS production

# Non-root user
RUN useradd --create-home appuser
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application files
COPY --chown=appuser:appuser . .

# Create model + data directories (the app user must be able to write to them)
RUN mkdir -p models data && chown appuser:appuser models data

USER appuser

# Train the baseline at build time so the image ships a model and /health is "ok"
# (needs internet during the build to download the ~0.5 MB sentiment dataset)
RUN python main.py

EXPOSE 8005

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8005/health')"

# One worker: metrics, the prediction log and rate-limit counters live in process memory,
# so several workers would each keep their own (split) numbers. Scale with more containers
# plus shared storage (e.g. Prometheus multiprocess mode, a Redis-backed limiter) instead.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "1"]
