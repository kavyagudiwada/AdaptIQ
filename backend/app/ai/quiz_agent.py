"""Quiz agent: generates difficulty-matched practice questions."""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from app.ai import prompts
from app.ai.demo_content import GENERIC_QUIZ_BANK, QUIZ_BANK
from app.ai.llm_service import generate_json_or_none
from app.core.config import settings
from app.utils.curriculum import display_name, subtopics_for

logger = logging.getLogger(__name__)

QUESTION_COUNT = 4


def _stable_offset(seed: str, modulo: int) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % max(1, modulo)


def _validate(raw: Any, difficulty: str) -> list[dict[str, Any]] | None:
    if not isinstance(raw, list) or not raw:
        return None

    cleaned: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            return None
        question = str(item.get("question", "")).strip()
        options = item.get("options")
        correct = item.get("correct_index")
        if not question or not isinstance(options, list) or len(options) != 4:
            return None
        if not isinstance(correct, int) or not 0 <= correct <= 3:
            return None

        item_difficulty = str(item.get("difficulty", difficulty)).lower()
        if item_difficulty not in ("easy", "medium", "hard"):
            item_difficulty = difficulty

        cleaned.append(
            {
                "question": question,
                "options": [str(o).strip() for o in options],
                "correct_index": correct,
                "subtopic": str(item.get("subtopic", "")).strip() or "General",
                "difficulty": item_difficulty,
                "explanation": str(item.get("explanation", "")).strip()
                or "Review this concept once more and try a similar question.",
            }
        )
    return cleaned


def _localise(question: dict[str, Any], subtopic: str) -> dict[str, Any]:
    """Name the learner's actual subtopic inside a generic question.

    Topics without curated entries still get questions that read as specific to
    them, instead of "the core idea of this topic".
    """
    text = question["question"]
    for placeholder in ("this topic", "this area", "this concept", "a topic"):
        text = text.replace(placeholder, subtopic)
    return {**question, "question": text}


def _tiers_for(subtopic: str, difficulty: str) -> list[list[list[dict[str, Any]]]]:
    """Candidate pools grouped into ordered tiers of decreasing topical fit.

    Tier 0 is the exact subtopic/difficulty pair, tier 1 keeps the same subtopic
    at neighbouring levels, and only then do we fall back to the generic bank.
    Never mixing a tier means a curated subtopic always fills its set with
    on-topic questions before generic ones are considered.
    """
    sub_map = QUIZ_BANK.get(subtopic.strip().lower(), {})
    others = [level for level in ("easy", "medium", "hard") if level != difficulty]
    return [
        [sub_map.get(difficulty, [])],
        [sub_map.get(level, []) for level in others],
        [[_localise(q, subtopic) for q in GENERIC_QUIZ_BANK.get(difficulty, [])]],
        [
            [_localise(q, subtopic) for q in GENERIC_QUIZ_BANK.get(level, [])]
            for level in others
        ],
    ]


def _pick_demo(
    *, topic: str, subtopic: str, difficulty: str, seed: str
) -> list[dict[str, Any]]:
    """Choose offline questions for the requested subtopic + difficulty.

    Tops up from the same subtopic (other levels) and then the generic bank when
    the curated bank is smaller than a full set, so a quiz always has
    QUESTION_COUNT distinct questions at the difficulty the learner was assigned.
    """
    # Rotate within a tier (so two learners get different supporting questions)
    # but never across tiers, so on-topic questions always win over generic ones.
    pools: list[list[dict[str, Any]]] = []
    for tier_index, tier in enumerate(_tiers_for(subtopic, difficulty)):
        filled = [pool for pool in tier if pool]
        if not filled:
            continue
        if len(filled) > 1:
            offset = _stable_offset(
                f"{seed}:{subtopic}:{difficulty}:tier{tier_index}", len(filled)
            )
            filled = filled[offset:] + filled[:offset]
        pools.extend(filled)

    if not pools:
        pools = [GENERIC_QUIZ_BANK["medium"]]

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    for pool in pools:
        start = _stable_offset(
            f"{seed}:{subtopic}:{difficulty}:{len(selected)}", len(pool)
        )
        for question in pool[start:] + pool[:start]:
            text = question["question"]
            if text in seen:
                continue
            seen.add(text)
            selected.append(question)
            if len(selected) == QUESTION_COUNT:
                break
        if len(selected) == QUESTION_COUNT:
            break

    # Defensive: never return a short set even if the bank is exhausted.
    while len(selected) < QUESTION_COUNT:
        filler = _localise(
            GENERIC_QUIZ_BANK["medium"][len(selected) % QUESTION_COUNT], subtopic
        )
        selected.append(filler)
        seen.add(filler["question"])

    return [
        {
            "id": f"quiz-{i + 1}",
            "question": q["question"],
            "options": q["options"],
            "correct_index": q["correct_index"],
            "subtopic": subtopic,
            # Keep the question's real level. When we top up from a neighbouring
            # level the set is still centred on the assigned difficulty, but the
            # per-question badge stays honest.
            "difficulty": str(q.get("difficulty", difficulty)).lower(),
            "explanation": q["explanation"],
        }
        for i, q in enumerate(selected[:QUESTION_COUNT])
    ]


async def generate_questions(
    *,
    learner_id: int,
    topic: str,
    subtopic: str,
    difficulty: str,
    level: str,
    weak: list[str],
    seed: str | None = None,
) -> tuple[list[dict[str, Any]], str]:
    """Return (questions, ai_mode)."""
    if not subtopic:
        subtopic = subtopics_for(topic)[0]

    payload = await generate_json_or_none(
        prompts.QUIZ_SYSTEM,
        prompts.quiz_prompt(
            count=QUESTION_COUNT,
            topic=topic,
            subtopic=subtopic,
            difficulty=difficulty,
            level=level,
            weak=weak,
        ),
        # Temperature 0 makes live regeneration at submit time reproduce the
        # same paper, so answers are graded against the questions the learner
        # actually saw (the LLM path beyond the API is still overridable).
        temperature=0.0,
    )

    questions = _validate(payload.get("questions") if payload else None, difficulty)
    if questions:
        return (
            [
                {**q, "id": f"q{i + 1}", "subtopic": subtopic}
                for i, q in enumerate(questions[:QUESTION_COUNT])
            ],
            "live",
        )

    if settings.ai_enabled:
        logger.info("Quiz generation fell back to the offline bank.")
    # A fresh seed (sent on every "New set") rotates the deterministic offline
    # pick so a learner who clicks again gets a genuinely different set.
    rotation = f":{seed}" if seed else ""
    return (
        _pick_demo(
            topic=topic,
            subtopic=subtopic,
            difficulty=difficulty,
            seed=f"{learner_id}:{display_name(topic)}{rotation}",
        ),
        "offline",
    )
