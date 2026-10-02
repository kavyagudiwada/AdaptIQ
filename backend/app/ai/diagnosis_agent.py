"""Diagnosis agent: misconception tracing and confidence calibration.

Every wrong answer is traced to the specific misconception behind it (with a
concrete fix), and every rated attempt gets calibration coaching. Both paths are
LLM-first and fall back to deterministic rules so an empty key never breaks the
flow.
"""

from __future__ import annotations

import logging
from typing import Any

from app.ai import prompts
from app.ai.llm_service import generate_json_or_none
from app.core.config import settings

logger = logging.getLogger(__name__)


def _fallback_misconceptions(
    wrong: list[dict[str, Any]],
) -> dict[str, dict[str, str]]:
    """Deterministic diagnosis: anchored to the question's own explanation."""
    result: dict[str, dict[str, str]] = {}
    for q in wrong:
        result[q["question_id"]] = {
            "misconception": (
                f"An unclear or incomplete understanding of {q['subtopic']} - the "
                f"chosen option repeats a common pattern for this concept, so the "
                f"underlying mental model needs revisiting."
            ),
            "fix": q["explanation"] or "Re-read the linked concept and rework this question.",
        }
    return result


async def diagnose_misconceptions(
    *,
    topic: str,
    subtopic: str,
    level: str,
    learner_id: int,
    wrong: list[dict[str, Any]],
) -> tuple[dict[str, dict[str, str]], str]:
    """Return ({question_id: {misconception, fix}}, ai_mode)."""
    if not wrong:
        return {}, "offline"

    payload = await generate_json_or_none(
        prompts.MISCONCEPTION_SYSTEM,
        prompts.misconception_prompt(
            topic=topic, subtopic=subtopic, level=level, wrong_questions=wrong
        ),
        temperature=0.4,
    )

    if payload:
        items = payload.get("misconceptions")
        if isinstance(items, list):
            valid_ids = {q["question_id"] for q in wrong}
            cleaned: dict[str, dict[str, str]] = {}
            for item in items:
                if not isinstance(item, dict):
                    continue
                qid = str(item.get("question_id", "")).strip()
                if qid not in valid_ids:
                    continue
                misconception = str(item.get("misconception", "")).strip()
                fix = str(item.get("fix", "")).strip()
                if misconception:
                    cleaned[qid] = {
                        "misconception": misconception,
                        "fix": fix or "Re-read this subtopic and rework the question.",
                    }
            if cleaned:
                return cleaned, "live"

    if settings.ai_enabled:
        logger.info("Misconception diagnosis fell back to deterministic rules.")
    return _fallback_misconceptions(wrong), "offline"


def _fallback_calibration(
    *,
    confidence_avg: float,
    accuracy: float,
    gap: float,
    answered_count: int,
) -> str:
    if answered_count == 0:
        return (
            "Rate how sure you are on each question next time, and we will coach "
            "your confidence to match your real accuracy."
        )
    if gap >= 20:
        return (
            f"You felt {confidence_avg:.0f}% sure but scored {accuracy:.0f}% - you "
            "were overconfident. Before submitting, re-check each 'confident' answer "
            "against the question wording; trust decreases when you can explain why."
        )
    if gap >= 5:
        return (
            f"You were slightly overconfident ({confidence_avg:.0f}% confidence vs "
            f"{accuracy:.0f}% accuracy). Re-read questions you flagged as sure before "
            "submitting and look for traps."
        )
    if gap <= -20:
        return (
            f"You scored {accuracy:.0f}% but only felt {confidence_avg:.0f}% sure - "
            "you know more than you trust. Attempt the question first, then reflect "
            "on the evidence before judging yourself."
        )
    if gap < -5:
        return (
            f"Your confidence ({confidence_avg:.0f}%) trailed your performance "
            f"({accuracy:.0f}%). Log the specific reasons your answer is right so "
            "your confidence reflects evidence, not doubt."
        )
    return (
        f"Your confidence ({confidence_avg:.0f}%) closely matched your performance "
        f"({accuracy:.0f}%). Keep rating honestly each attempt to stay calibrated."
    )


async def calibration_feedback(
    *,
    name: str,
    level: str,
    topic: str,
    confidence_avg: float,
    accuracy: float,
    gap: float,
    answered_count: int,
) -> tuple[str, str]:
    """Return (feedback, ai_mode)."""
    if answered_count == 0:
        return _fallback_calibration(
            confidence_avg=confidence_avg,
            accuracy=accuracy,
            gap=gap,
            answered_count=0,
        ), "offline"

    payload = await generate_json_or_none(
        prompts.CALIBRATION_SYSTEM,
        prompts.calibration_prompt(
            name=name,
            level=level,
            topic=topic,
            confidence_avg=confidence_avg,
            accuracy=accuracy,
            gap=gap,
            answered_count=answered_count,
        ),
        temperature=0.4,
    )
    if payload:
        feedback = str(payload.get("feedback", "")).strip()
        if feedback:
            return feedback, "live"

    if settings.ai_enabled:
        logger.info("Calibration feedback fell back to deterministic rules.")
    return (
        _fallback_calibration(
            confidence_avg=confidence_avg,
            accuracy=accuracy,
            gap=gap,
            answered_count=answered_count,
        ),
        "offline",
    )


__all__ = ["diagnose_misconceptions", "calibration_feedback"]