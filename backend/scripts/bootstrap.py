"""Dev bootstrap for AdaptIQ.

Creates the PostgreSQL database if it does not exist yet, then applies all
Alembic migrations. Used by `run.bat` / `run.sh` so a fresh clone can go from
checkout to running servers in one command.

Databases must be created by an admin (``postgres``) connection, so this script
connects to the maintenance database using the same host, port and credentials
from ``DATABASE_URL`` and issues ``CREATE DATABASE`` only if it is missing.
"""

from __future__ import annotations

import asyncio
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import asyncpg
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/learnai",
)


def target_database() -> str:
    parsed = urlparse(DATABASE_URL)
    return (parsed.path.lstrip("/").split("/")[0] or "learnai")


def admin_url() -> str:
    """Same URL pointed at the ``postgres`` maintenance database."""
    parsed = urlparse(DATABASE_URL)
    return urlunparse(
        (
            parsed.scheme.replace("+asyncpg", ""),
            parsed.netloc,
            "/postgres",
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )


def masked_location() -> str:
    parsed = urlparse(DATABASE_URL)
    return f"{parsed.hostname or 'localhost'}:{parsed.port or 5432}"


async def ensure_database() -> None:
    """Connect as the admin user; CREATE DATABASE when the app DB is missing."""
    try:
        conn = await asyncpg.connect(admin_url())
    except Exception as exc:  # unreachable / auth failure / wrong port
        print(f"[bootstrap] could not connect to PostgreSQL at {masked_location()}")
        print(f"[bootstrap] {exc}")
        print("[bootstrap]  - is PostgreSQL running?")
        print("[bootstrap]  - is DATABASE_URL in backend/.env correct?")
        print("[bootstrap]  - cloud instances may not allow CREATE DATABASE")
        raise SystemExit(1)

    db = target_database()
    try:
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db
        )
        if exists:
            print(f"[bootstrap] database '{db}' already exists")
            return
        try:
            await conn.execute(f'CREATE DATABASE "{db}"')
            print(f"[bootstrap] created database '{db}'")
        except asyncpg.InsufficientPrivilegeError:
            print(f"[bootstrap] cannot create '{db}' (no CREATEDB privilege).")
            print(f"[bootstrap] create it manually:  CREATE DATABASE {db};")
            raise SystemExit(1)
    finally:
        await conn.close()


def apply_migrations() -> None:
    print("[bootstrap] applying migrations...")
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(BACKEND_DIR),
        text=True,
    )
    if result.returncode == 0:
        print("[bootstrap] schema is up to date.")
    else:
        print("[bootstrap] WARNING: alembic did not complete — see output above.")
        raise SystemExit(result.returncode)


def main() -> None:
    print("[bootstrap] AdaptIQ backend setup")
    asyncio.run(ensure_database())
    apply_migrations()


if __name__ == "__main__":
    main()