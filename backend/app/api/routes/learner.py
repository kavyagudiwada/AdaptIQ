"""Learner profile endpoints."""

from fastapi import APIRouter, status

from app.core.database import DbSession
from app.schemas.learner import LearnerProfileCreate, LearnerProfileOut
from app.services.assessment_service import get_learner_or_404

router = APIRouter(prefix="/learner", tags=["learner"])


@router.post(
    "/profile", response_model=LearnerProfileOut, status_code=status.HTTP_201_CREATED
)
async def create_profile(
    payload: LearnerProfileCreate, session: DbSession
) -> LearnerProfileOut:
    """Create a learner profile. Each save starts a fresh learner record."""
    from app.models import Learner

    learner = Learner(
        name=payload.name.strip(),
        topic=payload.topic.strip(),
        current_level=payload.current_level,
        # Freeze the claim; `current_level` becomes the measured level once
        # there is evidence, and this is what we compare against.
        self_reported_level=payload.current_level,
        learning_goal=payload.learning_goal,
        hours_per_week=payload.hours_per_week,
        target_duration=payload.target_duration,
    )
    session.add(learner)
    await session.commit()
    await session.refresh(learner)
    return LearnerProfileOut.model_validate(learner)


@router.get("/{learner_id}", response_model=LearnerProfileOut)
async def read_learner(learner_id: int, session: DbSession) -> LearnerProfileOut:
    learner = await get_learner_or_404(session, learner_id)
    return LearnerProfileOut.model_validate(learner)
