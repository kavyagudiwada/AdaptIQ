"""Health endpoint used by the frontend and by judges to verify the stack."""

from fastapi import APIRouter

from app.core.config import settings
from app.core.database import check_database
from app.schemas.progress import HealthOut

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthOut)
async def health() -> HealthOut:
    db_status = await check_database()
    return HealthOut(
        status="ok" if db_status == "connected" else "degraded",
        database=db_status,
        ai_provider=settings.ai_provider,
        ai_mode=settings.ai_mode,  # type: ignore[arg-type]
        version=settings.version,
    )
