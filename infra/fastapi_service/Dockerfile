# ─────────────────────────────────────────────
# Stage: base — общие зависимости
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
# Stage: builder — сборка зависимостей
# ─────────────────────────────────────────────
FROM base AS builder

COPY requirements.txt requirements-dev.txt ./

RUN pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# ─────────────────────────────────────────────
# Stage: development — с dev-зависимостями и hot-reload
# ─────────────────────────────────────────────
FROM base AS development

COPY --from=builder /install /usr/local

RUN pip install --no-cache-dir \
    pytest \
    pytest-asyncio \
    pytest-cov \
    httpx \
    respx \
    fakeredis \
    watchfiles

COPY . .

EXPOSE 8000

# ─────────────────────────────────────────────
# Stage: production
# ─────────────────────────────────────────────
FROM base AS production

COPY --from=builder /install /usr/local

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
