"""Assessment orchestration: generate paper, score submission, persist results."""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai import assessment_agent
from app.models import Assessment, Learner, Progress
from app.schemas.assessment import (
    AssessmentPaperOut,
    AssessmentResultOut,
    AssessmentSubmitRequest,
    TopicBreakdown,
)
from app.utils.curriculum import subtopics_for
from app.utils.helpers import estimate_level, mastery_for
from app.services.adaptation_service import refresh_learner_level

logger = logging.getLogger(__name__)

ASSESSMENT_SUBJECT = "Initial assessment"


async def get_learner_or_404(session: AsyncSession, learner_id: int) -> Learner:
    learner = await session.get(Learner, learner_id)
    if learner is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=f"Learner {learner_id} not found.")
    return learner


async def generate_paper(
    session: AsyncSession, learner_id: int
) -> AssessmentPaperOut:
    learner = await get_learner_or_404(session, learner_id)

    questions, ai_mode = await assessment_agent.generate_paper(
        learner_id=learner.id,
        topic=learner.topic,
        level=learner.current_level,
        goal=learner.learning_goal,
    )

    return AssessmentPaperOut(
        assessment_id=None,
        learner_id=learner.id,
        questions=questions,
        total_questions=len(questions),
        ai_mode=ai_mode,
    )


async def submit_assessment(
    session: AsyncSession, payload: AssessmentSubmitRequest
) -> AssessmentResultOut:
    learner = await get_learner_or_404(session, payload.learner_id)

    # The paper is regenerated deterministically so we can grade it server-side.
    # In a real deployment this would be read from a stored paper table.
    questions, ai_mode = await assessment_agent.generate_paper(
        learner_id=learner.id,
        topic=learner.topic,
        level=learner.current_level,
        goal=learner.learning_goal,
    )
    by_id = {q["id"]: q for q in questions}

    score = 0
    graded = 0
    per_subtopic: dict[str, dict[str, int]] = {}

    for answer in payload.answers:
        question = by_id.get(answer.question_id)
        if question is None:
            # Ignore answers to questions we no longer recognise.
            continue
        graded += 1
        bucket = per_subtopic.setdefault(
            question["subtopic"], {"correct": 0, "total": 0}
        )
        bucket["total"] += 1
        if answer.selected_index == question["correct_index"]:
            score += 1
            bucket["correct"] += 1

    if graded == 0:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail="None of the submitted answers matched the generated assessment.",
        )

    percentage = round(score / graded * 100, 1)

    breakdown = [
        TopicBreakdown(
            subtopic=sub,
            correct=data["correct"],
            total=data["total"],
            percentage=round(data["correct"] / data["total"] * 100, 1),
        )
        for sub, data in per_subtopic.items()
    ]

    analysis, analysis_mode = await assessment_agent.analyse_result(
        name=learner.name,
        topic=learner.topic,
        level=learner.current_level,
        percentage=percentage,
        per_subtopic=[
            {
                "subtopic": b.subtopic,
                "correct": b.correct,
                "total": b.total,
                "percentage": b.percentage,
            }
            for b in breakdown
        ],
    )

    # Deterministic level estimate wins over the model's guess.
    level = estimate_level(percentage, learner.current_level)

    assessment = Assessment(
        learner_id=learner.id,
        score=score,
        total_questions=graded,
        strong_topics=analysis["strong_topics"],
        weak_topics=analysis["weak_topics"],
    )
    session.add(assessment)
    learner.estimated_level = level
    await session.flush()

    # Seed per-subtopic progress rows so the dashboard has something to show.
    for item in breakdown:
        progress = await _get_or_create_progress(session, learner.id, item.subtopic)
        progress.last_score = item.percentage
        progress.progress_percentage = item.percentage
        progress.mastery_level = mastery_for(item.percentage)

    # Close the feedback loop: a graded assessment is our strongest evidence, so
    # it rewrites the learner's *effective* level. The self-report is preserved
    # separately, and every downstream consumer (quizzes, papers, roadmap,
    # tutor) reads current_level and therefore gets the measured value.
    previous_level = learner.current_level
    await refresh_learner_level(session, learner)

    await session.commit()
    await session.refresh(assessment)

    logger.info(
        "Assessment %s for learner %s: %s/%s (%s%%) mode=%s, level %s -> %s",
        assessment.id,
        learner.id,
        score,
        graded,
        percentage,
        analysis_mode,
        previous_level,
        learner.current_level,
    )

    return AssessmentResultOut(
        assessment_id=assessment.id,
        learner_id=learner.id,
        score=score,
        total_questions=graded,
        percentage=percentage,
        strong_topics=analysis["strong_topics"],
        weak_topics=analysis["weak_topics"],
        estimated_level=level,
        topic_breakdown=breakdown,
        feedback=analysis["feedback"],
        ai_mode=ai_mode if ai_mode == "live" else analysis_mode,
    )


async def _get_or_create_progress(
    session: AsyncSession, learner_id: int, topic: str
) -> Progress:
    result = await session.execute(
        select(Progress).where(
            Progress.learner_id == learner_id, Progress.topic == topic
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    progress = Progress(
        learner_id=learner_id,
        topic=topic,
        progress_percentage=0.0,
        mastery_level="beginner",
        last_score=0.0,
    )
    session.add(progress)
    return progress


async def latest_assessment(session: AsyncSession, learner_id: int) -> Assessment | None:
    result = await session.execute(
        select(Assessment)
        .where(Assessment.learner_id == learner_id)
        .order_by(Assessment.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()
