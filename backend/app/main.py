"""LearnAI FastAPI application entrypoint."""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import (
    assessment,
    auth,
    health,
    learner,
    progress,
    quiz,
    roadmap,
    tutor,
)
from app.core.config import settings
from app.core.database import dispose_engine, engine
from app.models import (  # noqa: F401
    Account,
    Assessment,
    Learner,
    Progress,
    QuizAttempt,
    Roadmap,
)

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger("learnai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s v%s", settings.app_name, settings.version)
    logger.info("AI provider: %s | mode: %s", settings.ai_provider, settings.ai_mode)
    if not settings.ai_enabled:
        logger.warning(
            "No AI_API_KEY configured - running in DEMO/FALLBACK mode. "
            "All features work with curated offline content."
        )
    try:
        async with engine.connect() as conn:
            await conn.exec_driver_sql("SELECT 1")
        logger.info("PostgreSQL connection OK")
    except Exception as exc:  # noqa: BLE001
        logger.error("PostgreSQL connection FAILED: %s", exc)
        logger.error("Check DATABASE_URL in backend/.env and run: alembic upgrade head")
    yield
    await dispose_engine()
    logger.info("Shutdown complete")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=(
        "Personalised AI Tutor for learning AI. "
        "Assessment -> Personalisation -> Roadmap -> Tutor -> Adaptive Practice -> Progress."
    ),
    lifespan=lifespan,
)

# CORS: the frontend is a local dev server, so allow any loopback port (Vite
# falls back to 5174+ when 5173 is taken) plus any extra origins listed in
# FRONTEND_URL (comma separated). Loopback-only, so this stays local-safe.
_extra_origins = [
    origin.strip() for origin in settings.frontend_url.split(",") if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_origins=[*_extra_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api"

app.include_router(health.router, prefix=API_PREFIX)
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(learner.router, prefix=API_PREFIX)
app.include_router(assessment.router, prefix=API_PREFIX)
app.include_router(roadmap.router, prefix=API_PREFIX)
app.include_router(tutor.router, prefix=API_PREFIX)
app.include_router(quiz.router, prefix=API_PREFIX)
app.include_router(progress.router, prefix=API_PREFIX)


# --- Optional: serve the built SPA from the API ----------------------------
# When FRONTEND_DIR points at a `npm run build` output (frontend/dist), the
# API also hosts the React app so the whole product lives behind one URL. This
# is how production/Render deployments run; /api/* keeps routing to the API.
_frontend_dir = Path(settings.frontend_dir).resolve() if settings.frontend_dir else None
_frontend_index = (
    (_frontend_dir / "index.html")
    if _frontend_dir and (_frontend_dir / "index.html").is_file()
    else None
)

if _frontend_index is not None and _frontend_dir is not None:
    # Real files from the build (hashed assets + anything copied from public/
    # e.g. img src="/studify.png") must return their actual bytes, so an <img>
    # gets a PNG image/response. The catch-all below serves files first and
    # only falls back to index.html for genuinely missing SPA routes. It is
    # registered after the API routers, so /api/* is unaffected.
    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_files(full_path: str):
        # Unknown /api/* paths that dodge every router must 404, not return
        # the SPA. /docs and /openapi.json are registered earlier by FastAPI,
        # so they never reach this catch-all.
        if full_path.startswith(API_PREFIX.lstrip("/")):
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "Not found"},
            )

        from fastapi.responses import FileResponse

        candidate = (_frontend_dir / full_path).resolve()
        if candidate.is_relative_to(_frontend_dir) and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(_frontend_index)

    logger.info("Serving frontend from %s", _frontend_dir)


@app.get("/", include_in_schema=False)
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": settings.version,
        "docs": "/docs",
        "health": f"{API_PREFIX}/health",
    }


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all so unexpected errors never leak internals to the client."""
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred. Please try again.",
            "path": request.url.path,
        },
    )
