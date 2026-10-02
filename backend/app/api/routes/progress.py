"""Progress dashboard endpoint."""

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DbSession
from app.schemas.progress import ProgressOut
from app.services.progress_service import get_progress

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/{learner_id}", response_model=ProgressOut)
async def read(learner_id: int, session: DbSession) -> ProgressOut:
    """Return topic mastery, history, streak and the recommended next topic."""
    return await get_progress(session, learner_id)
