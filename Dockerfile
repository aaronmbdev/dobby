# ── Client builder ────────────────────────────────────────────────────────────
FROM node:22-slim AS client-builder

WORKDIR /client

COPY client/package.json client/package-lock.json* ./
RUN npm ci

COPY client ./
RUN npm run build

# ── Python builder ─────────────────────────────────────────────────────────────
FROM python:3.14-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install dependencies into an isolated venv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# ── Runtime ───────────────────────────────────────────────────────────────────
FROM python:3.14-slim AS runtime

WORKDIR /app

# Copy venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code and Alembic resources
COPY src ./src
COPY project ./project
COPY alembic.ini ./alembic.ini

# Copy compiled React app from client builder
COPY --from=client-builder /client/dist ./client/dist

# Make the venv's binaries available on PATH
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
