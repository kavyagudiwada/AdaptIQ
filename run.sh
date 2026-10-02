#!/usr/bin/env bash
# ============================================================
#  AdaptIQ - one-command local setup (macOS / Linux)
#  Creates the venv, installs deps, prepares the database,
#  applies migrations and starts backend + frontend.
# ============================================================
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo
echo "  ============================================"
echo "    AdaptIQ - one-command local setup"
echo "  ============================================"
echo

command -v python3 >/dev/null 2>&1 || { echo "[ERROR] python3 not found on PATH."; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "[ERROR] npm not found on PATH."; exit 1; }

PY="$ROOT/backend/.venv/bin/python"

if [ ! -x "$PY" ]; then
  echo "[1/4] Creating Python virtual environment..."
  python3 -m venv "$ROOT/backend/.venv"
fi

echo "[2/4] Installing Python dependencies..."
"$PY" -m pip install --quiet --disable-pip-version-check -r "$ROOT/backend/requirements.txt"

[ -f "$ROOT/backend/.env" ] || cp "$ROOT/backend/.env.example" "$ROOT/backend/.env"
[ -f "$ROOT/frontend/.env" ] || cp "$ROOT/frontend/.env.example" "$ROOT/frontend/.env"

echo "[3/4] Preparing the database..."
"$PY" "$ROOT/backend/scripts/bootstrap.py"

if [ ! -d "$ROOT/frontend/node_modules" ]; then
  echo "[4/4] Installing frontend dependencies..."
  (cd "$ROOT/frontend" && npm install --no-fund --no-audit)
else
  echo "[4/4] Frontend dependencies already installed."
fi

echo
echo "  Starting servers..."
(cd "$ROOT/backend" && "$PY" -m uvicorn app.main:app --reload --port 8000) &
BACK_PID=$!
(cd "$ROOT/frontend" && npm run dev) &
FRONT_PID=$!

trap 'kill $BACK_PID $FRONT_PID 2>/dev/null || true' EXIT INT TERM

echo "  Backend : http://localhost:8000/api/health"
echo "  Frontend: http://localhost:5173"
echo "  Press Ctrl+C to stop both servers."
wait