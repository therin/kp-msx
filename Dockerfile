# kp-msx — Kinopub → Media Station X bridge.
# Self-hosted for the LG C5 in Tomsk (russia2026 move project).
# Hosting decision + deploy runbook: homelab repo `kp-msx-hosting/README.md`
# (Fly.io EU, SQLite on a Fly Volume, no Cloudflare).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080 \
    SQLITE_URL=/data/kp.db

WORKDIR /app

# Install deps first so the layer caches across source edits.
COPY requirements.txt .
RUN pip install -r requirements.txt

# App source.
COPY . .

# SQLite DB lives on a mounted volume in production (Fly Volume -> /data).
# The mount shadows this dir at runtime; the mkdir just covers a bare `docker run`.
RUN mkdir -p /data

EXPOSE 8080

# Honor an injected $PORT (Fly/Render set it); default 8080.
CMD ["sh", "-c", "exec uvicorn --host 0.0.0.0 --port ${PORT} api:app"]
