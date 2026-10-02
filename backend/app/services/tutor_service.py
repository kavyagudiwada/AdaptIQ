"""Tutor orchestration: gather full learner context, then explain."""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai import tutor_agent
from app.models import Progress, QuizAttempt, TutorSession
from app.schemas.tutor import (
    TutorExplainRequest,
    TutorHistoryItem,
    TutorHistoryOut,
    TutorResponseOut,
)
from app.services.assessment_service import get_learner_or_404, latest_assessment
from app.services.roadmap_service import get_roadmap
from app.utils.curriculum import subtopics_for

logger = logging.getLogger(__name__)


async def _recent_scores(session: AsyncSession, learner_id: int, limit: int = 3) -> str:
    result = await session.execute(
        select(QuizAttempt)
        .where(QuizAttempt.learner_id == learner_id)
        .order_by(QuizAttempt.created_at.desc())
        .limit(limit)
    )
    attempts = result.scalars().all()
    if not attempts:
        return "Recent scores: none yet."
    parts = [
        f"{a.topic} {a.percentage:.0f}% ({a.difficulty})" for a in reversed(attempts)
    ]
    return "Recent quiz scores: " + ", ".join(parts)


async def _weak_topics(session: AsyncSession, learner_id: int) -> tuple[list[str], list[str]]:
    result = await session.execute(
        select(Progress).where(Progress.learner_id == learner_id)
    )
    rows = result.scalars().all()
    if not rows:
        return [], []
    strong = [r.topic for r in rows if r.last_score >= 75]
    weak = [r.topic for r in rows if r.last_score < 60]
    return strong, weak


async def explain(
    session: AsyncSession, payload: TutorExplainRequest
) -> TutorResponseOut:
    learner = await get_learner_or_404(session, payload.learner_id)

    # Personalisation inputs: weak topics, roadmap position, recent scores.
    strong, weak = await _weak_topics(session, learner.id)
    recent = await _recent_scores(session, learner.id)
    assessment = await latest_assessment(session, learner.id)
    if assessment and not weak:
        weak = list(assessment.weak_topics)
    if assessment and not strong:
        strong = list(assessment.strong_topics)

    roadmap = await get_roadmap(session, learner.id)
    roadmap_week: int | None = None
    if roadmap and roadmap.weeks:
        roadmap_week = roadmap.weeks[0].week

    # Resolve the requested topic to a known subtopic where possible.
    requested = (payload.topic or "").strip()
    known = subtopics_for(learner.topic)
    match = next((s for s in known if s.lower() == requested.lower()), None)
    subtopic = match or requested or known[0]

    body, ai_mode = await tutor_agent.explain(
        name=learner.name,
        topic=learner.topic,
        subtopic=subtopic,
        level=learner.current_level,
        goal=learner.learning_goal,
        estimated_level=learner.estimated_level,
        strong=strong,
        weak=weak,
        recent_scores=recent,
        learner_question=payload.question or "",
        roadmap_week=roadmap_week,
    )

    logger.info("Tutor explained %r for learner %s (mode=%s)", subtopic, learner.id, ai_mode)

    # Persist the session so progress can count real tutor sessions and the
    # learner keeps a record of what they were taught.
    session.add(
        TutorSession(
            learner_id=learner.id,
            topic=learner.topic,
            subtopic=subtopic,
            question=payload.question or None,
            difficulty=body.get("difficulty", "medium"),
            explanation=body["explanation"],
            example=body.get("example", ""),
            key_points=body.get("key_points"),
            common_mistakes=body.get("common_mistakes"),
            follow_up_question=body.get("follow_up_question"),
            personalized_note=body.get("personalized_note"),
            ai_mode=ai_mode,
        )
    )
    await session.commit()

    return TutorResponseOut(**body, ai_mode=ai_mode)


async def history(
    session: AsyncSession, learner_id: int, limit: int = 15
) -> TutorHistoryOut:
    """Saved explanations for a learner, newest first."""
    result = await session.execute(
        select(TutorSession)
        .where(TutorSession.learner_id == learner_id)
        .order_by(TutorSession.created_at.desc())
        .limit(limit)
    )
    rows = result.scalars().all()
    return TutorHistoryOut(
        sessions=[
            TutorHistoryItem(
                id=s.id,
                topic=s.topic,
                subtopic=s.subtopic,
                difficulty=s.difficulty,  # type: ignore[arg-type]
                explanation=s.explanation,
                example=s.example,
                key_points=s.key_points or [],
                common_mistakes=s.common_mistakes or [],
                ai_mode=s.ai_mode or "offline",  # type: ignore[arg-type]
                created_at=s.created_at,
            )
            for s in rows
        ]
    )
