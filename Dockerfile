# AdaptIQ - production image.
#
# One image, one URL: this build compiles the React app and lets the FastAPI
# backend serve both the SPA (frontend/dist) and the /api endpoints. Used by
# Render (render.yaml) and usable with plain `docker build`.
#
#   docker build -t adaptiq:latest .
#   docker run --rm -p 8000:8000 -e DATABASE_URL=... adaptiq:latest

# ---- Stage 1: build the frontend ------------------------------------------
FROM node:20-alpine AS frontend-build

WORKDIR /web

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --no-fund --no-audit

COPY frontend/ ./
# VITE_API_URL left unset => the app talks to the same origin (/api).
RUN npm run build

# ---- Stage 2: Python backend + built SPA ----------------------------------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY backend/alembic ./alembic
COPY backend/alembic.ini .

# Built SPA, served by the API at /.
COPY --from=frontend-build /web/dist ./web
ENV FRONTEND_DIR=/app/web

EXPOSE 8000

# Migrate the schema, then serve API + SPA. DATABASE_URL comes from the host
# (Render injects `postgres://...` which config normalises to +asyncpg).
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]