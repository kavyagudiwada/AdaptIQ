"""Assessment agent: generates the diagnostic quiz and analyses the result.

Falls back to the offline bank whenever the LLM is unavailable.
"""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from app.ai import prompts
from app.ai.demo_content import ASSESSMENT_BANK
from app.ai.llm_service import generate_json_or_none
from app.core.config import settings
from app.utils.curriculum import display_name, normalise_topic, subtopics_for

logger = logging.getLogger(__name__)

QUESTION_COUNT = 5


def _stable_offset(seed: str, modulo: int) -> int:
    """Deterministic per-learner rotation so demo mode is not identical twice."""
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % max(1, modulo)


def _validate_questions(raw: Any, subtopics: list[str]) -> list[dict[str, Any]] | None:
    """Reject malformed LLM output so we never store broken questions."""
    if not isinstance(raw, list) or not raw:
        return None

    cleaned: list[dict[str, Any]] = []
    allowed = {s.lower() for s in subtopics}

    for item in raw:
        if not isinstance(item, dict):
            return None
        question = str(item.get("question", "")).strip()
        options = item.get("options")
        correct = item.get("correct_index")
        subtopic = str(item.get("subtopic", "")).strip()
        difficulty = str(item.get("difficulty", "medium")).strip().lower()

        if not question or not isinstance(options, list) or len(options) != 4:
            return None
        if not isinstance(correct, int) or not 0 <= correct <= 3:
            return None
        if difficulty not in ("easy", "medium", "hard"):
            difficulty = "medium"
        if subtopic.lower() not in allowed:
            subtopic = subtopics[0]

        cleaned.append(
            {
                "question": question,
                "options": [str(o).strip() for o in options],
                "correct_index": correct,
                "subtopic": subtopic,
                "difficulty": difficulty,
            }
        )
    return cleaned


RANK = {"easy": 0, "medium": 1, "hard": 2}


def _level_sort_key(question: dict[str, Any], level: str) -> tuple[int, int]:
    """Order the bank so a beginner meets the easy end and an advanced the hard end.

    The sort is stable, so the per-learner rotation still varies questions within
    a difficulty band.
    """
    rank = RANK.get(str(question.get("difficulty", "medium")).lower(), 1)
    if level == "advanced":
        return (-rank, rank)
    if level == "intermediate":
        return (abs(rank - 1), rank)
    return (rank, rank)


def _demo_paper(topic: str, level: str, seed: str) -> list[dict[str, Any]]:
    """Offline assessment: rotate through the bank so each learner differs."""
    key = normalise_topic(topic)
    bank = ASSESSMENT_BANK.get(key, [])
    if not bank:
        bank = _synthesise_generic(topic, subtopics_for(topic))

    start = _stable_offset(f"{seed}:{key}", len(bank))
    order = bank[start:] + bank[:start]

    # The declared level decides which end of the bank the learner meets first.
    order.sort(key=lambda q: _level_sort_key(q, level))

    picked: list[dict[str, Any]] = []
    seen_subtopics: set[str] = set()
    for q in order:
        if q["subtopic"] not in seen_subtopics:
            picked.append(q)
            seen_subtopics.add(q["subtopic"])
        if len(picked) == QUESTION_COUNT:
            break
    for q in order:
        if len(picked) == QUESTION_COUNT:
            break
        if q not in picked:
            picked.append(q)

    return [
        {
            "id": f"demo-{i + 1}",
            "question": q["question"],
            "options": q["options"],
            "correct_index": q["correct_index"],
            "subtopic": q["subtopic"],
            "difficulty": q["difficulty"],
        }
        for i, q in enumerate(picked[:QUESTION_COUNT])
    ]


def _synthesise_generic(topic: str, subtopics: list[str]) -> list[dict[str, Any]]:
    """Build a small generic bank for topics not covered by the curated bank."""
    made: list[dict[str, Any]] = []
    for i, sub in enumerate(subtopics[:10]):
        made.append(
            {
                "question": f"In {display_name(topic)}, what does '{sub}' primarily cover?",
                "options": [
                    f"The core ideas and practice of {sub}",
                    "Unrelated hardware maintenance",
                    "Database administration only",
                    "Network configuration only",
                ],
                "correct_index": 0,
                "subtopic": sub,
                "difficulty": ["easy", "medium", "hard"][i % 3],
            }
        )
    return made


async def generate_paper(
    *, learner_id: int, topic: str, level: str, goal: str
) -> tuple[list[dict[str, Any]], str]:
    """Return (questions, ai_mode) for the initial assessment."""
    subtopics = subtopics_for(topic)

    payload = await generate_json_or_none(
        prompts.ASSESSMENT_GENERATION_SYSTEM,
        prompts.assessment_generation_prompt(
            count=QUESTION_COUNT,
            topic=topic,
            level=level,
            goal=goal,
            subtopics=subtopics,
        ),
    )

    questions = _validate_questions(payload.get("questions") if payload else None, subtopics)
    if questions:
        return (
            [
                {**q, "id": f"q{i + 1}"} for i, q in enumerate(questions[:QUESTION_COUNT])
            ],
            "live",
        )

    if settings.ai_enabled:
        logger.info("Assessment generation fell back to the local content bank.")
    return _demo_paper(topic, level, seed=str(learner_id)), "offline"


def _demo_analysis(
    *, name: str, percentage: float, per_subtopic: list[dict[str, Any]]
) -> dict[str, Any]:
    strong = [r["subtopic"] for r in per_subtopic if r["percentage"] >= 100]
    weak = [r["subtopic"] for r in per_subtopic if r["percentage"] < 100]

    if percentage >= 75:
        level = "advanced"
    elif percentage >= 45:
        level = "intermediate"
    else:
        level = "beginner"

    if weak:
        focus = ", ".join(weak[:3])
        message = (
            f"Nice work, {name}. You scored {percentage}%. "
            f"We will spend extra time on {focus} before moving faster."
        )
    else:
        message = (
            f"Excellent, {name}. You scored {percentage}% with no weak areas detected, "
            "so your roadmap will skip the basics and move straight to harder material."
        )

    return {
        "estimated_level": level,
        "strong_topics": strong,
        "weak_topics": weak,
        "feedback": message,
    }


async def analyse_result(
    *,
    name: str,
    topic: str,
    level: str,
    percentage: float,
    per_subtopic: list[dict[str, Any]],
) -> tuple[dict[str, Any], str]:
    """Return ({estimated_level, strong_topics, weak_topics, feedback}, ai_mode)."""
    payload = await generate_json_or_none(
        prompts.ASSESSMENT_ANALYSIS_SYSTEM,
        prompts.assessment_analysis_prompt(
            name=name,
            level=level,
            topic=topic,
            score_pct=percentage,
            per_subtopic=per_subtopic,
        ),
    )

    if payload:
        estimated = str(payload.get("estimated_level", "")).lower()
        if estimated in ("beginner", "intermediate", "advanced"):
            strong = [str(t) for t in payload.get("strong_topics", [])]
            weak = [str(t) for t in payload.get("weak_topics", [])]
            feedback = str(payload.get("feedback", "")).strip()
            if strong or weak or feedback:
                return (
                    {
                        "estimated_level": estimated,
                        "strong_topics": strong,
                        "weak_topics": weak,
                        "feedback": feedback or "Assessment complete.",
                    },
                    "live",
                )

    if settings.ai_enabled:
        logger.info("Assessment analysis fell back to deterministic logic.")
    return (
        _demo_analysis(name=name, percentage=percentage, per_subtopic=per_subtopic),
        "offline",
    )
