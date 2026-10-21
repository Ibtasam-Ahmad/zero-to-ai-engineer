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

# Create model directory
RUN mkdir -p models && chown appuser:appuser models

USER appuser

EXPOSE 8005

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8005/health')"

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8005", "--workers", "2"]
