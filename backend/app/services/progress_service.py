"""Progress aggregation: topic mastery, history, streak and next-step advice."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai import prompts
from app.ai.llm_service import generate_json_or_none
from app.core.config import settings
from app.models import Assessment, Learner, Progress, QuizAttempt, Roadmap, TutorSession
from app.schemas.progress import (
    ActivityItem,
    ProgressOut,
    QuizHistoryPoint,
    TopicProgressOut,
)
from app.utils.curriculum import subtopics_for
from app.utils.helpers import clamp

logger = logging.getLogger(__name__)

HISTORY_LIMIT = 15
ACTIVITY_LIMIT = 8


def _as_aware(value: datetime) -> datetime:
    """Postgres returns tz-aware datetimes, but be defensive anyway."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _learning_streak(dates: list[date]) -> int:
    """Consecutive days ending today (or yesterday) with recorded activity."""
    if not dates:
        return 0
    unique = sorted(set(dates), reverse=True)
    today = datetime.now(timezone.utc).date()

    if unique[0] not in (today, today - timedelta(days=1)):
        return 0

    streak = 1
    for i in range(1, len(unique)):
        if unique[i - 1] - unique[i] == timedelta(days=1):
            streak += 1
        else:
            break
    return streak


async def _offline_recommendation(
    *, topic_scores: list[dict], allowed: list[str]
) -> tuple[str, str, str]:
    if not topic_scores:
        return (
            allowed[0] if allowed else "Start with the fundamentals",
            "No recorded performance yet, so start with the first topic in your roadmap.",
            allowed[0] if allowed else "Fundamentals",
        )

    ranked = sorted(topic_scores, key=lambda r: r["last_score"])
    weakest = ranked[0]
    if weakest["last_score"] < 60:
        return (
            weakest["topic"],
            f"Your recent performance indicates that {weakest['topic']} needs more practice "
            f"(last score {weakest['last_score']:.0f}%). Complete the recommended practice set "
            "before moving to the next topic.",
            weakest["topic"],
        )

    # Everything is reasonably strong: advance to the next unexplored topic.
    covered = {r["topic"] for r in topic_scores}
    nxt = next((a for a in allowed if a not in covered), None)
    if nxt:
        return (
            nxt,
            f"All tracked topics are above 60%, so you are ready to move on to {nxt}.",
            ranked[-1]["topic"],
        )
    return (
        ranked[-1]["topic"],
        f"{ranked[-1]['topic']} is your strongest topic at {ranked[-1]['last_score']:.0f}%. "
        "Keep pushing it toward advanced difficulty.",
        ranked[-1]["topic"],
    )


async def get_progress(session: AsyncSession, learner_id: int) -> ProgressOut:
    learner = await session.get(Learner, learner_id)
    if learner is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=f"Learner {learner_id} not found.")

    progress_rows = (
        (
            await session.execute(
                select(Progress)
                .where(Progress.learner_id == learner_id)
                .order_by(Progress.updated_at.desc())
            )
        )
        .scalars()
        .all()
    )

    assessment = (
        (
            await session.execute(
                select(Assessment)
                .where(Assessment.learner_id == learner_id)
                .order_by(Assessment.created_at.desc())
                .limit(1)
            )
        )
        .scalar_one_or_none()
    )

    attempts = (
        (
            await session.execute(
                select(QuizAttempt)
                .where(QuizAttempt.learner_id == learner_id)
                .order_by(QuizAttempt.created_at.desc())
                .limit(HISTORY_LIMIT)
            )
        )
        .scalars()
        .all()
    )

    tutor_sessions = (
        (
            await session.execute(
                select(TutorSession)
                .where(TutorSession.learner_id == learner_id)
                .order_by(TutorSession.created_at.desc())
                .limit(HISTORY_LIMIT)
            )
        )
        .scalars()
        .all()
    )

    roadmap = (
        (
            await session.execute(
                select(Roadmap)
                .where(Roadmap.learner_id == learner_id)
                .order_by(Roadmap.created_at.desc())
                .limit(1)
            )
        )
        .scalar_one_or_none()
    )

    topics = [
        TopicProgressOut(
            topic=r.topic,
            progress_percentage=round(r.progress_percentage, 1),
            mastery_level=r.mastery_level,  # type: ignore[arg-type]
            last_score=round(r.last_score, 1),
            updated_at=r.updated_at,
        )
        for r in progress_rows
    ]

    topic_scores = [
        {
            "topic": r.topic,
            "last_score": r.last_score,
            "mastery_level": r.mastery_level,
            "progress_percentage": r.progress_percentage,
        }
        for r in progress_rows
    ]

    overall = (
        round(sum(t.progress_percentage for t in topics) / len(topics), 1)
        if topics
        else 0.0
    )

    calibration_scores = [abs(a.calibration_gap) for a in attempts if a.calibration_gap is not None]
    calibration_avg_gap = (
        round(sum(calibration_scores) / len(calibration_scores), 1)
        if calibration_scores
        else None
    )

    strong = [r.topic for r in progress_rows if r.last_score >= 75]
    weak = [r.topic for r in progress_rows if r.last_score < 60]
    if not weak and assessment:
        weak = list(assessment.weak_topics)
    if not strong and assessment:
        strong = list(assessment.strong_topics)

    # Next-step recommendation (AI, falling back to a deterministic rule).
    allowed = subtopics_for(learner.topic)
    recommended = ""
    reason = ""
    current = ""
    ai_mode = "offline"

    if topic_scores:
        payload = await generate_json_or_none(
            prompts.PERFORMANCE_SYSTEM,
            prompts.performance_prompt(
                name=learner.name,
                topic=learner.topic,
                level=learner.estimated_level or learner.current_level,
                goal=learner.learning_goal,
                allowed=allowed,
                topic_scores=topic_scores,
            ),
        )
        if payload:
            recommended = str(payload.get("recommended_next_topic", "")).strip()
            reason = str(payload.get("recommendation_reason", "")).strip()
            current = str(payload.get("current_topic", "")).strip()
            if recommended and reason:
                ai_mode = "live"

    if not recommended:
        recommended, reason, current = await _offline_recommendation(
            topic_scores=topic_scores, allowed=allowed
        )
        if settings.ai_enabled:
            logger.info("Progress recommendation fell back to deterministic logic.")

    if not current:
        current = topics[0].topic if topics else allowed[0]

    # Activity feed + streak.
    activity: list[ActivityItem] = []
    activity_dates: list[date] = [_as_aware(a.created_at).date() for a in attempts]
    if assessment:
        activity.append(
            ActivityItem(
                label="Initial assessment completed",
                detail=f"Scored {assessment.percentage:.0f}% · level {assessment.estimated_level}",
                kind="assessment",
                created_at=assessment.created_at,
            )
        )
        activity_dates.append(_as_aware(assessment.created_at).date())
    if roadmap:
        activity.append(
            ActivityItem(
                label="Roadmap generated",
                detail=roadmap.title,
                kind="roadmap",
                created_at=roadmap.created_at,
            )
        )
        activity_dates.append(_as_aware(roadmap.created_at).date())
    for attempt in attempts[:5]:
        activity.append(
            ActivityItem(
                label=f"Quiz · {attempt.topic}",
                detail=f"{attempt.percentage:.0f}% at {attempt.difficulty} difficulty",
                kind="quiz",
                created_at=attempt.created_at,
            )
        )
    for session_entry in tutor_sessions[:5]:
        activity.append(
            ActivityItem(
                label=f"Tutor · {session_entry.subtopic}",
                detail="Explanation saved to your history",
                kind="tutor",
                created_at=session_entry.created_at,
            )
        )
        activity_dates.append(_as_aware(session_entry.created_at).date())
    activity.append(
        ActivityItem(
            label="Profile created",
            detail=f"{learner.name} · {learner.topic}",
            kind="profile",
            created_at=learner.created_at,
        )
    )
    activity_dates.append(_as_aware(learner.created_at).date())
    activity.sort(key=lambda a: _as_aware(a.created_at), reverse=True)

    return ProgressOut(
        learner_id=learner.id,
        learner_name=learner.name,
        topic=learner.topic,
        overall_progress=clamp(overall),
        assessment_percentage=assessment.percentage if assessment else None,
        estimated_level=(assessment.estimated_level if assessment else learner.estimated_level)
        or learner.current_level,  # type: ignore[arg-type]
        current_topic=current,
        recommended_next_topic=recommended,
        recommendation_reason=reason,
        topics=topics,
        strong_topics=strong,
        weak_topics=weak,
        quiz_history=[
            QuizHistoryPoint(
                attempt_id=a.id,
                topic=a.topic,
                difficulty=a.difficulty,  # type: ignore[arg-type]
                percentage=a.percentage,
                confidence_avg=round(a.confidence_avg, 1) if a.confidence_avg is not None else None,
                calibration_gap=round(a.calibration_gap, 1) if a.calibration_gap is not None else None,
                created_at=a.created_at,
            )
            for a in reversed(attempts)
        ],
        calibration_avg_gap=calibration_avg_gap,
        learning_streak=_learning_streak(activity_dates),
        total_quizzes=len(attempts),
        total_tutor_sessions=len(tutor_sessions),
        roadmap_weeks_completed=roadmap.completed_weeks if roadmap else 0,
        recent_activity=activity[:ACTIVITY_LIMIT],
        ai_mode=ai_mode,  # type: ignore[arg-type]
    )
