# ─────────────────────────────────────────────
# Stage: base
# ─────────────────────────────────────────────
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────
# Stage: builder
# ─────────────────────────────────────────────
FROM base AS builder

COPY requirements.txt ./

RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# ─────────────────────────────────────────────
# Stage: development
# ─────────────────────────────────────────────
FROM base AS development

COPY --from=builder /install /usr/local

RUN pip install --no-cache-dir \
    pytest \
    pytest-django \
    pytest-cov \
    model-bakery

COPY . .

EXPOSE 8001

# ─────────────────────────────────────────────
# Stage: production
# ─────────────────────────────────────────────
FROM base AS production

COPY --from=builder /install /usr/local

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8001

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8001", "--workers", "2"]
