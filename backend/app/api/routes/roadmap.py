"""Roadmap endpoints."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DbSession
from app.schemas.roadmap import (
    AdaptationOut,
    RoadmapCompletionOut,
    RoadmapGenerateRequest,
    RoadmapOut,
)
from app.services.roadmap_service import (
    complete_week,
    generate_roadmap,
    get_adaptation_status,
    get_roadmap,
)

router = APIRouter(prefix="/roadmap", tags=["roadmap"])


@router.post("/generate", response_model=RoadmapOut, status_code=status.HTTP_200_OK)
async def generate(
    payload: RoadmapGenerateRequest, session: DbSession
) -> RoadmapOut:
    """Build a personalised week-by-week roadmap from the learner's results.

    Idempotent by default: if the plan already reflects the learner's latest
    evidence it is returned unchanged. Pass ``force=true`` to rebuild anyway.
    """
    return await generate_roadmap(session, payload)


@router.get("/{learner_id}/adaptation", response_model=AdaptationOut)
async def adaptation(learner_id: int, session: DbSession) -> AdaptationOut:
    """Report whether the active plan still matches the learner's results.

    This is what the roadmap screen polls so it can offer to adapt the plan
    rather than silently leaving the learner on a stale one.
    """
    return await get_adaptation_status(session, learner_id)


@router.post("/{learner_id}/week/complete", response_model=RoadmapCompletionOut)
async def week_complete(learner_id: int, session: DbSession) -> RoadmapCompletionOut:
    """Check off the next week of the learner's active roadmap."""
    return await complete_week(session, learner_id)


@router.get("/{learner_id}", response_model=RoadmapOut)
async def read(
    learner_id: int, session: DbSession
) -> RoadmapOut:
    """Return the learner's active roadmap, or 404 if none exists."""
    roadmap = await get_roadmap(session, learner_id)
    if roadmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No roadmap yet. Generate one after completing the assessment.",
        )
    return roadmap
