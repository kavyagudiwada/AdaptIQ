"""AI tutor endpoint."""

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DbSession
from app.schemas.tutor import (
    TutorExplainRequest,
    TutorHistoryOut,
    TutorResponseOut,
)
from app.services.tutor_service import explain, history

router = APIRouter(prefix="/tutor", tags=["tutor"])


@router.post("/explain", response_model=TutorResponseOut)
async def tutor_explain(
    payload: TutorExplainRequest, session: DbSession
) -> TutorResponseOut:
    """Explain a topic using the learner's level, goal, weak topics and scores."""
    return await explain(session, payload)


@router.get("/{learner_id}/history", response_model=TutorHistoryOut)
async def tutor_history(learner_id: int, session: DbSession) -> TutorHistoryOut:
    """Saved explanations for a learner, newest first."""
    return await history(session, learner_id)
