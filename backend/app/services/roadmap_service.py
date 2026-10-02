"""Roadmap orchestration: build a personalised plan and persist it."""

from __future__ import annotations

import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai import roadmap_agent
from app.models import Roadmap
from app.schemas.roadmap import (
    AdaptationOut,
    RoadmapCompletionOut,
    RoadmapGenerateRequest,
    RoadmapOut,
    RoadmapTopic,
    RoadmapWeek,
)
from app.services.adaptation_service import (
    AdaptationSnapshot,
    apply_snapshot,
    build_snapshot,
    refresh_learner_level,
)
from app.services.assessment_service import get_learner_or_404
from app.utils.helpers import LEVEL_RANK

logger = logging.getLogger(__name__)

# Roadmaps store their mode inside the JSON blob. Rows written before the
# fallback was renamed from "demo" to "offline" still carry the old value, so
# reads have to translate it rather than let the response schema reject it.
_LEGACY_AI_MODES = {"demo": "offline"}


def _stored_ai_mode(roadmap_data: dict | None) -> str:
    mode = (roadmap_data or {}).get("ai_mode") or "offline"
    return _LEGACY_AI_MODES.get(mode, mode)


def _to_out(
    roadmap: Roadmap,
    ai_mode: str,
    adaptation: AdaptationOut | None = None,
) -> RoadmapOut:
    data = roadmap.roadmap_data or {}
    return RoadmapOut(
        id=roadmap.id,
        learner_id=roadmap.learner_id,
        title=roadmap.title,
        duration=roadmap.duration,
        weeks=[RoadmapWeek(**week) for week in data.get("weeks", [])],
        personalization_notes=data.get("personalization_notes", []),
        focus_areas=roadmap.focus_areas or data.get("focus_areas", []),
        ai_mode=ai_mode,
        created_at=roadmap.created_at,
        revision=roadmap.revision or 1,
        superseded=bool(roadmap.superseded),
        completed_weeks=roadmap.completed_weeks or 0,
        adaptation_reason=roadmap.adaptation_reason,
        adaptation=adaptation,
    )


def _adaptation_out(
    snapshot: AdaptationSnapshot,
    stored_signature: str | None,
    revision: int = 0,
) -> AdaptationOut:
    current = snapshot.signature()
    return AdaptationOut(
        is_stale=stored_signature is not None and stored_signature != current,
        revision=revision,
        effective_level=snapshot.level,
        self_reported_level=snapshot.self_reported_level,
        level_source=snapshot.level_source,  # type: ignore[arg-type]
        level_changed_from_start=snapshot.level != snapshot.self_reported_level,
        average_mastery=snapshot.average_mastery,
        total_attempts=snapshot.total_attempts,
        weak_topics=snapshot.weak,
        strong_topics=snapshot.strong,
        reasons=snapshot.reasons(),
        basis_signature=stored_signature,
        current_signature=current,
    )


async def current_roadmap_row(session: AsyncSession, learner_id: int) -> Roadmap | None:
    """The learner's active plan - the newest one not yet superseded."""
    result = await session.execute(
        select(Roadmap)
        .where(Roadmap.learner_id == learner_id, Roadmap.superseded.is_(False))
        .order_by(Roadmap.revision.desc(), Roadmap.created_at.desc())
        .limit(1)
    )
    return result.scalars().first()


async def get_adaptation_status(
    session: AsyncSession, learner_id: int
) -> AdaptationOut:
    """Compare the active plan against the learner's latest evidence."""
    learner = await get_learner_or_404(session, learner_id)
    snapshot = await apply_snapshot(session, learner, await build_snapshot(session, learner))
    active = await current_roadmap_row(session, learner_id)
    return _adaptation_out(
        snapshot,
        active.basis_signature if active else None,
        (active.revision or 1) if active else 0,
    )


async def generate_roadmap(
    session: AsyncSession, payload: RoadmapGenerateRequest
) -> RoadmapOut:
    learner = await get_learner_or_404(session, payload.learner_id)

    # Close the loop: the level the plan is built on is the measured one.
    snapshot = await refresh_learner_level(session, learner)

    active = await current_roadmap_row(session, learner.id)
    signature = snapshot.signature()

    # Idempotent by default - don't rebuild a plan that still matches reality.
    if active is not None and not payload.force and active.basis_signature == signature:
        logger.info(
            "Roadmap for learner %s is current (rev=%s); returning as-is",
            learner.id,
            active.revision,
        )
        return _to_out(
            active,
            _stored_ai_mode(active.roadmap_data),
            _adaptation_out(snapshot, active.basis_signature, active.revision or 1),
        )

    # Work out *why* we are rebuilding, in words the learner can read.
    previous_level = active and (active.roadmap_data or {}).get("level")
    reason = _describe_rebuild(snapshot, previous_level)
    reasons = snapshot.reasons(previous_level)

    plan, ai_mode = await roadmap_agent.generate_roadmap(
        name=learner.name,
        topic=learner.topic,
        level=snapshot.level,
        goal=learner.learning_goal,
        hours_per_week=learner.hours_per_week,
        weeks=learner.target_duration,
        score=snapshot.assessment_score,
        strong=snapshot.strong,
        weak=snapshot.weak,
    )

    roadmap = Roadmap(
        learner_id=learner.id,
        title=plan["title"],
        duration=learner.target_duration,
        roadmap_data={"weeks": plan["weeks"]},
        focus_areas=plan.get("focus_areas", []),
        revision=(active.revision + 1) if active else 1,
        basis_signature=signature,
        superseded=False,
        adaptation_reason=reason,
    )
    # Personalisation notes live inside the JSON blob so they survive a round-trip.
    roadmap.roadmap_data["personalization_notes"] = plan.get("personalization_notes", [])
    roadmap.roadmap_data["ai_mode"] = ai_mode
    # Record the level the plan was actually built on, so the next rebuild can
    # explain a level change even after several revisions.
    roadmap.roadmap_data["level"] = snapshot.level
    roadmap.roadmap_data["weak_topics"] = snapshot.weak
    roadmap.roadmap_data["strong_topics"] = snapshot.strong

    # Retire the old plan instead of orphaning it with a bare INSERT.
    if active is not None:
        await session.execute(
            update(Roadmap)
            .where(Roadmap.id == active.id)
            .values(superseded=True)
        )

    session.add(roadmap)
    await session.commit()
    await session.refresh(roadmap)

    logger.info(
        "Roadmap %s rev=%s for learner %s (mode=%s, level=%s, weak=%s): %s",
        roadmap.id,
        roadmap.revision,
        learner.id,
        ai_mode,
        snapshot.level,
        snapshot.weak,
        reason,
    )
    return _to_out(roadmap, ai_mode, _adaptation_out(snapshot, signature, roadmap.revision))


def _describe_rebuild(
    snapshot: AdaptationSnapshot, previous_level: str | None
) -> str:
    if not previous_level:
        return "First personalised plan built from your assessment and practice history."

    bits: list[str] = []
    if snapshot.level != previous_level:
        moved = "up" if LEVEL_RANK[snapshot.level] > LEVEL_RANK[previous_level] else "down"
        bits.append(f"level {previous_level} -> {snapshot.level} ({moved})")
    if snapshot.weak:
        bits.append(f"weak topics: {', '.join(snapshot.weak[:3])}")
    if snapshot.strong:
        bits.append(f"strong topics: {', '.join(snapshot.strong[:3])}")
    if not bits:
        bits.append("practice results updated")
    return "Adapted - " + "; ".join(bits)


async def get_roadmap(session: AsyncSession, learner_id: int) -> RoadmapOut | None:
    roadmap = await current_roadmap_row(session, learner_id)
    if roadmap is None:
        return None

    ai_mode = _stored_ai_mode(roadmap.roadmap_data)
    adaptation = await get_adaptation_status(session, learner_id)
    return _to_out(roadmap, ai_mode, adaptation)


def first_topic_of(roadmap: RoadmapOut) -> str:
    for week in roadmap.weeks:
        for topic in week.topics:
            return topic.name
    return ""


async def complete_week(
    session: AsyncSession, learner_id: int
) -> RoadmapCompletionOut:
    """Mark the learner's active roadmap one week further along."""
    roadmap = await current_roadmap_row(session, learner_id)
    if roadmap is None:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No roadmap yet. Generate one after completing the assessment.",
        )

    next_weeks = min(roadmap.duration, (roadmap.completed_weeks or 0) + 1)
    roadmap.completed_weeks = next_weeks
    await session.commit()
    await session.refresh(roadmap)
    return RoadmapCompletionOut(
        completed_weeks=next_weeks,
        duration=roadmap.duration,
        completed=next_weeks >= roadmap.duration,
    )


def all_topic_names(roadmap: RoadmapOut) -> list[str]:
    names: list[str] = []
    for week in roadmap.weeks:
        for topic in week.topics:
            if topic.name not in names:
                names.append(topic.name)
    return names


__all__ = [
    "generate_roadmap",
    "get_roadmap",
    "get_adaptation_status",
    "current_roadmap_row",
    "complete_week",
    "first_topic_of",
    "all_topic_names",
    "RoadmapTopic",
]
