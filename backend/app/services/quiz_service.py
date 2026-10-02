"""Quiz orchestration, including the adaptive difficulty engine.

Adaptive rules (spec section 16), intentionally simple and transparent:
    score < 50        -> easy
    50 <= score < 75  -> medium
    score >= 75       -> hard
"""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai import diagnosis_agent, quiz_agent
from app.models import Progress, QuizAttempt, Roadmap
from app.schemas.quiz import (
    MisconceptionOut,
    QuizAnswer,
    QuizGenerateRequest,
    QuizOut,
    QuizQuestionOut,
    QuizResultOut,
    QuizReviewItem,
    QuizSubmitRequest,
)
from app.services.assessment_service import get_learner_or_404
from app.utils.curriculum import subtopics_for
from app.utils.helpers import clamp, difficulty_rank, mastery_for, next_difficulty
from app.services.adaptation_service import refresh_learner_level

logger = logging.getLogger(__name__)

ADAPTATION_MESSAGES = {
    "up": (
        "Great improvement. You scored {score:.0f}% on {topic}, so you are ready for "
        "application-based problems. Increasing difficulty from {current} to {next}."
    ),
    "same": (
        "Your performance in {topic} is {band} ({score:.0f}%). Keeping the difficulty at "
        "{next} to consolidate this topic with more targeted practice."
    ),
    "down": (
        "Your performance in {topic} is {band} ({score:.0f}%). Let's strengthen the "
        "fundamentals, so we are reducing the difficulty from {current} to {next} and "
        "adding more explanations."
    ),
}

BAND_TEXT = {
    "easy": "below expectations",
    "medium": "moderate",
    "hard": "strong",
}


def adaptation_note(
    *, topic: str, previous: float | None, difficulty: str
) -> str:
    """Human-readable explanation of why this difficulty was chosen."""
    if previous is None:
        return (
            f"Starting at {difficulty} difficulty based on your profile. "
            "After this attempt we will adapt automatically."
        )
    expected = next_difficulty(previous)
    if expected == difficulty:
        return (
            f"Your last score on {topic} was {previous:.0f}%, which maps to {difficulty} "
            "difficulty. Keeping it steady to consolidate."
        )
    direction = "up" if difficulty == "hard" else "down"
    return (
        f"Your last score on {topic} was {previous:.0f}% → that maps to {expected} difficulty. "
        f"Adapting to {difficulty} for this attempt."
    )


def system_message(
    *, topic: str, score: float, current: str, next_diff: str
) -> str:
    """Describe the difficulty transition the learner just earned."""
    band = BAND_TEXT[next_difficulty(score)]

    if next_diff == current:
        key = "same"
    elif difficulty_rank(next_diff) > difficulty_rank(current):
        key = "up"
    else:
        key = "down"

    return ADAPTATION_MESSAGES[key].format(
        topic=topic, score=score, band=band, current=current, next=next_diff
    )


def previous_difficulty(previous: float | None) -> str:
    if previous is None:
        return "medium"
    return next_difficulty(previous)


async def _last_percentage(
    session: AsyncSession, learner_id: int, topic: str
) -> float | None:
    result = await session.execute(
        select(QuizAttempt)
        .where(QuizAttempt.learner_id == learner_id, QuizAttempt.topic == topic)
        .order_by(QuizAttempt.created_at.desc())
        .limit(1)
    )
    attempt = result.scalar_one_or_none()
    return attempt.percentage if attempt else None


async def _weak_topics(session: AsyncSession, learner_id: int) -> list[str]:
    result = await session.execute(
        select(Progress).where(Progress.learner_id == learner_id)
    )
    rows = result.scalars().all()
    return [r.topic for r in rows if r.last_score < 60]


async def _recommended_difficulty(
    session: AsyncSession, learner_id: int, topic: str
) -> tuple[str, float | None]:
    previous = await _last_percentage(session, learner_id, topic)
    if previous is None:
        # No history for this topic: fall back to the weakest recorded topic so
        # the learner is pushed toward their actual gap.
        result = await session.execute(
            select(Progress)
            .where(Progress.learner_id == learner_id)
            .order_by(Progress.last_score.asc())
            .limit(1)
        )
        weakest = result.scalar_one_or_none()
        if weakest and weakest.last_score > 0:
            return next_difficulty(weakest.last_score), None
        return "medium", None
    return next_difficulty(previous), previous


async def generate_quiz(
    session: AsyncSession, payload: QuizGenerateRequest
) -> QuizOut:
    learner = await get_learner_or_404(session, payload.learner_id)

    topic = (payload.topic or "").strip()
    if not topic:
        known = subtopics_for(learner.topic)
        progress_result = await session.execute(
            select(Progress)
            .where(Progress.learner_id == learner.id)
            .order_by(Progress.last_score.asc())
            .limit(1)
        )
        weakest = progress_result.scalar_one_or_none()
        topic = weakest.topic if weakest else known[0]

    difficulty, previous = await _recommended_difficulty(session, learner.id, topic)
    weak = await _weak_topics(session, learner.id)

    questions, ai_mode = await quiz_agent.generate_questions(
        learner_id=learner.id,
        topic=learner.topic,
        subtopic=topic,
        difficulty=difficulty,
        level=learner.current_level,
        weak=weak,
        seed=payload.seed,
    )

    return QuizOut(
        quiz_id=None,
        learner_id=learner.id,
        topic=topic,
        difficulty=difficulty,
        questions=[QuizQuestionOut(**q) for q in questions],
        total_questions=len(questions),
        adaptation_note=adaptation_note(
            topic=topic, previous=previous, difficulty=difficulty
        ),
        previous_percentage=previous,
        ai_mode=ai_mode,
    )


async def submit_quiz(
    session: AsyncSession, payload: QuizSubmitRequest
) -> QuizResultOut:
    learner = await get_learner_or_404(session, payload.learner_id)

    # Grade against the exact paper the learner answered whenever the client
    # sends it back (the LLM path must not be re-rolled after the fact). Older
    # clients fall back to a deterministic regeneration.
    paper: list[dict] | None = None
    ai_mode = "offline"
    if payload.paper:
        paper = [q.model_dump() for q in payload.paper]
        graded_difficulty = payload.difficulty
        ai_mode = payload.ai_mode or "offline"
    else:
        difficulty, _ = await _recommended_difficulty(
            session, learner.id, payload.topic
        )
        graded_difficulty = (
            difficulty if difficulty == payload.difficulty else payload.difficulty
        )
        weak = await _weak_topics(session, learner.id)

        questions, ai_mode = await quiz_agent.generate_questions(
            learner_id=learner.id,
            topic=learner.topic,
            subtopic=payload.topic,
            difficulty=graded_difficulty,
            level=learner.current_level,
            weak=weak,
        )
        paper = questions

    by_id = {q["id"]: q for q in paper}

    score = 0
    graded = 0
    answer_map: dict[str, int] = {}
    confidence_map: dict[str, int] = {}
    review_rows: list[dict] = []
    wrong_rows: list[dict] = []

    for answer in payload.answers:
        question = by_id.get(answer.question_id)
        if question is None:
            continue
        graded += 1
        answer_map[answer.question_id] = answer.selected_index
        if answer.selected_index is not None and answer.confidence is not None:
            confidence_map[answer.question_id] = answer.confidence

        correct = answer.selected_index == question["correct_index"]
        if correct:
            score += 1

        review_rows.append(
            {
                "question_id": answer.question_id,
                "question": question["question"],
                "subtopic": question.get("subtopic") or payload.topic,
                "your_answer": question["options"][answer.selected_index],
                "correct_answer": question["options"][question["correct_index"]],
                "was_correct": correct,
                "explanation": question.get("explanation", ""),
            }
        )
        if not correct:
            wrong_rows.append(
                {
                    "question_id": answer.question_id,
                    "question": question["question"],
                    "options": question["options"],
                    "selected_index": answer.selected_index,
                    "correct_index": question["correct_index"],
                    "subtopic": question.get("subtopic") or payload.topic,
                    "explanation": question.get("explanation", ""),
                }
            )

    if graded == 0:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail="None of the submitted answers matched the generated quiz.",
        )

    percentage = round(score / graded * 100, 1)
    next_diff = next_difficulty(percentage)
    previous = await _last_percentage(session, learner.id, payload.topic)

    # --- Confidence calibration -----------------------------------------
    confidence_avg: float | None = None
    calibration_gap: float | None = None
    calibration_feedback: str | None = None
    if confidence_map:
        confidence_avg = round(
            sum(confidence_map.values()) / len(confidence_map) * 20, 1
        )
        calibration_gap = round(confidence_avg - percentage, 1)
        calibration_feedback, _ = await diagnosis_agent.calibration_feedback(
            name=learner.name,
            level=learner.current_level,
            topic=payload.topic,
            confidence_avg=confidence_avg,
            accuracy=percentage,
            gap=calibration_gap,
            answered_count=len(confidence_map),
        )

    # --- Misconception diagnosis -----------------------------------------
    misconceptions, _ = await diagnosis_agent.diagnose_misconceptions(
        topic=learner.topic,
        subtopic=payload.topic,
        level=learner.current_level,
        learner_id=learner.id,
        wrong=wrong_rows,
    )
    for row in wrong_rows:
        entry = misconceptions.get(row["question_id"])
        row["misconception"] = entry["misconception"] if entry else None
        row["misconception_fix"] = entry["fix"] if entry else None

    for row in review_rows:
        if row["was_correct"]:
            continue
        entry = misconceptions.get(row["question_id"])
        row["misconception"] = entry["misconception"] if entry else None
        row["misconception_fix"] = entry["fix"] if entry else None

    attempt = QuizAttempt(
        learner_id=learner.id,
        topic=payload.topic,
        difficulty=graded_difficulty,
        score=score,
        total_questions=graded,
        answers=answer_map,
        confidence_avg=confidence_avg,
        calibration_gap=calibration_gap,
        misconceptions=misconceptions if misconceptions else None,
        calibration_feedback=calibration_feedback,
    )
    session.add(attempt)
    await session.flush()

    # Update (or create) the topic progress row.
    result = await session.execute(
        select(Progress).where(
            Progress.learner_id == learner.id, Progress.topic == payload.topic
        )
    )
    progress = result.scalar_one_or_none()
    if progress is None:
        progress = Progress(learner_id=learner.id, topic=payload.topic)
        session.add(progress)

    # Smooth the running average so one lucky attempt does not spike mastery.
    prior = progress.last_score or 0.0
    blended = 0.6 * percentage + 0.4 * prior if prior > 0 else percentage
    progress.last_score = percentage
    progress.progress_percentage = round(clamp(blended), 1)
    progress.mastery_level = mastery_for(blended)

    # Flush the new progress row so the adaptation snapshot can read it, then
    # let real practice results feed the learner's effective level. The
    # corroboration rule in the snapshot keeps a single set from flipping it.
    await session.flush()
    previous_level = learner.current_level
    snapshot = await refresh_learner_level(session, learner)

    await session.commit()
    await session.refresh(attempt)

    strong = [payload.topic] if percentage >= 75 else []
    weak_topics = [payload.topic] if percentage < 50 else []

    # Does the active plan still match the evidence it was built from? If not we
    # nudge the frontend so it can offer to adapt the roadmap.
    active_roadmap = (
        await session.execute(
            select(Roadmap)
            .where(
                Roadmap.learner_id == learner.id,
                Roadmap.superseded.is_(False),
            )
            .order_by(Roadmap.revision.desc(), Roadmap.created_at.desc())
            .limit(1)
        )
    ).scalars().first()
    roadmap_stale = bool(
        active_roadmap is not None
        and active_roadmap.basis_signature
        and active_roadmap.basis_signature != snapshot.signature()
    )

    if percentage < 50:
        action = (
            f"Revisit {payload.topic} with the AI Tutor, then retry this practice set "
            "at easy difficulty before moving on."
        )
    elif percentage < 75:
        action = (
            f"You're close. Focus on the concepts you missed in {payload.topic} and "
            "take another medium-difficulty set to push past 75%."
        )
    else:
        action = (
            f"{payload.topic} is mastered. Move to a harder, application-based set or "
            "advance to the next topic in your roadmap."
        )

    logger.info(
        "Quiz attempt %s: %s/%s (%s%%) %s -> next %s; level %s -> %s (%s)",
        attempt.id,
        score,
        graded,
        percentage,
        graded_difficulty,
        next_diff,
        previous_level,
        learner.current_level,
        snapshot.level_source,
    )

    return QuizResultOut(
        attempt_id=attempt.id,
        learner_id=learner.id,
        topic=payload.topic,
        difficulty=graded_difficulty,
        score=score,
        total_questions=graded,
        percentage=percentage,
        next_difficulty=next_diff,
        difficulty_changed=next_diff != graded_difficulty,
        system_message=system_message(
            topic=payload.topic,
            score=percentage,
            current=graded_difficulty,
            next_diff=next_diff,
        ),
        weak_topics=weak_topics,
        strong_topics=strong,
        recommended_action=action,
        ai_mode=ai_mode,
        current_level=learner.current_level,
        level_changed=previous_level != learner.current_level,
        level_source=snapshot.level_source,
        roadmap_stale=roadmap_stale,
        review=[QuizReviewItem(**row) for row in review_rows],
        misconceptions=[
            MisconceptionOut(
                question_id=row["question_id"],
                misconception=row["misconception"] or "Review this concept.",
                fix=row["misconception_fix"]
                or "Re-read the subtopic and rework the question.",
            )
            for row in wrong_rows
        ],
        confidence_avg=confidence_avg,
        calibration_gap=calibration_gap,
        calibration_feedback=calibration_feedback,
    )


__all__ = [
    "generate_quiz",
    "submit_quiz",
    "adaptation_note",
    "system_message",
    "previous_difficulty",
]
