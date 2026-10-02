"""Roadmap agent: builds a genuinely personalised week-by-week plan.

The offline generator is deterministic but still adapts to score, strong/weak
topics, level, goal, weekly hours and target duration, so two learners with
different profiles always get visibly different roadmaps.
"""

from __future__ import annotations

import logging
from typing import Any

from app.ai import prompts
from app.ai.llm_service import generate_json_or_none
from app.core.config import settings
from app.utils.curriculum import display_name, subtopics_for

logger = logging.getLogger(__name__)

# Practice targets scale inversely with ability, so weak learners get more reps.
BASE_PRACTICE = {"beginner": 18, "intermediate": 14, "advanced": 10}


def _tier_for(score: float | None, level: str) -> str:
    """Decide the content tier: 'foundation', 'core' or 'advanced'."""
    if score is None:
        return "foundation" if level == "beginner" else "core"
    if score >= 75:
        return "advanced"
    if score >= 50:
        return "core"
    return "foundation"


def _build_plan(
    *,
    topic: str,
    level: str,
    goal: str,
    weeks: int,
    hours_per_week: float,
    score: float | None,
    strong: list[str],
    weak: list[str],
) -> dict[str, Any]:
    """Deterministic, personalised roadmap used in demo mode (and as a fallback)."""
    subtopics = subtopics_for(topic)
    tier = _tier_for(score, level)
    weak_lower = {w.lower() for w in weak}
    strong_lower = {s.lower() for s in strong}

    if tier == "advanced":
        # Compress fundamentals: only revisit them briefly.
        ordered = [s for s in subtopics if s.lower() in weak_lower]
        ordered += [
            s
            for s in subtopics
            if s.lower() not in strong_lower and s.lower() not in weak_lower
        ]
        ordered += [s for s in subtopics if s.lower() in strong_lower]
    elif tier == "foundation":
        # Fundamentals first, weak topics early, strong topics only as light review.
        ordered = [s for s in subtopics if s.lower() not in strong_lower][:3]
        ordered += [s for s in subtopics if s.lower() in weak_lower]
        ordered += [s for s in subtopics if s.lower() not in strong_lower][3:]
        ordered += [s for s in subtopics if s.lower() in strong_lower]
    else:
        ordered = [s for s in subtopics if s.lower() in weak_lower]
        ordered += [s for s in subtopics if s.lower() not in strong_lower]
        ordered += [s for s in subtopics if s.lower() in strong_lower]

    # De-duplicate while keeping order.
    seen: set[str] = set()
    plan: list[str] = []
    for s in ordered:
        if s.lower() not in seen:
            seen.add(s.lower())
            plan.append(s)

    practice_base = BASE_PRACTICE.get(level, 14)
    notes: list[str] = []
    focus_areas: list[str] = []

    if tier == "advanced":
        notes.append(
            f"You scored {score}%, so fundamentals are compressed into a single "
            "revision block and the plan jumps to advanced, application-heavy work."
        )
    elif tier == "foundation":
        notes.append(
            f"You scored {score}%, so this plan front-loads fundamentals, adds worked "
            "examples and raises your weekly practice target to reinforce them."
        )
    elif score is not None:
        notes.append(
            f"You scored {score}%, so the plan follows the standard sequence but adds "
            "targeted practice on the topics you missed."
        )
    else:
        notes.append(
            "No assessment score yet, so this plan starts from fundamentals at a "
            "moderate pace and adapts once you take the assessment."
        )

    if weak:
        focus_areas.extend(weak[:4])
        notes.append(
            f"Weak areas scheduled early and repeated later: {', '.join(weak[:4])}."
        )
    if strong:
        notes.append(
            f"Already strong, so these get brief review only: {', '.join(strong[:4])}."
        )

    goal_note = {
        "placement": "Timed practice sets and company-style case questions added.",
        "interview": "Rapid-fire conceptual drills and mock interview rounds added.",
        "academic": "Syllabus coverage and exam-style questions prioritised.",
        "project": "Every module ends with something you can build and ship.",
        "general": "Balanced mix of reading, practice and small projects.",
    }[goal]
    notes.append(goal_note)

    # Distribute the ordered subtopics across the requested number of weeks.
    buckets: list[list[str]] = [[] for _ in range(weeks)]
    per_week = max(1, len(plan) // weeks + (1 if len(plan) % weeks else 0))
    idx = 0
    for w in range(weeks):
        take = per_week if w < weeks - 1 else len(plan) - idx
        take = max(0, take)
        buckets[w] = plan[idx : idx + take]
        idx += take

    week_titles = {
        "foundation": [
            "Foundations First",
            "Core Building Blocks",
            "Getting Comfortable",
            "Consolidation",
            "Into Real Practice",
            "Building Confidence",
        ],
        "core": [
            "Core Concepts",
            "Hands-On Fundamentals",
            "Applied Skills",
            "Practice & Patterns",
            "Toward Production",
            "Consolidation & Review",
        ],
        "advanced": [
            "Advanced Concepts",
            "Architecture & Trade-offs",
            "Optimisation",
            "Production Patterns",
            "Capstone & Interview",
            "Mastery & Extension",
        ],
    }[tier]

    out_weeks: list[dict[str, Any]] = []
    for w in range(weeks):
        items = buckets[w]
        week_practice = practice_base
        if tier == "foundation":
            week_practice = practice_base + 4
        # Weeks containing weak topics get extra targeted practice.
        if any(s.lower() in weak_lower for s in items):
            week_practice += 4

        topics = []
        for s in items:
            is_weak = s.lower() in weak_lower
            is_strong = s.lower() in strong_lower
            if tier == "advanced":
                difficulty = "hard" if not is_weak else "medium"
            elif tier == "foundation":
                difficulty = "easy" if is_weak else "medium"
            else:
                difficulty = "medium" if not is_weak else "easy"

            if is_weak:
                why = f"Your assessment showed weakness here, so it gets extra practice and an earlier slot."
            elif is_strong:
                why = f"You already scored well here, so this is a short confidence refresher."
            elif tier == "advanced":
                why = "Advanced material that builds directly on what you already know."
            else:
                why = "Core building block needed for everything that follows."

            topics.append(
                {
                    "name": s,
                    "subtopic": s,
                    "difficulty": difficulty,
                    "estimated_hours": round(hours_per_week / max(1, len(items)), 1),
                    "why_this_matters": why,
                    "resources": [
                        f"Read a concise guide on {s}",
                        f"Hands-on notebook exercise for {s}",
                    ],
                }
            )

        if not topics:
            topics.append(
                {
                    "name": "Consolidation review",
                    "subtopic": "Review",
                    "difficulty": "easy" if tier != "advanced" else "hard",
                    "estimated_hours": round(hours_per_week, 1),
                    "why_this_matters": "Reinforces the previous weeks before you move on.",
                    "resources": ["Mixed-topic practice set", "Self-check quiz"],
                }
            )

        focus = ", ".join(items) if items else "Consolidation"
        milestone = (
            f"Complete {week_practice} practice questions and explain {focus} without notes."
        )
        if w == weeks - 1:
            milestone = (
                "Finish with a mini-project and a mock review covering the whole plan."
            )

        out_weeks.append(
            {
                "week": w + 1,
                "title": week_titles[w % len(week_titles)],
                "focus": focus,
                "topics": topics,
                "practice_target": week_practice,
                "milestone": milestone,
            }
        )

    if tier == "advanced":
        title = f"{display_name(topic)} — Accelerated Track"
    elif tier == "foundation":
        title = f"{display_name(topic)} — Foundations-First Track"
    else:
        title = f"{display_name(topic)} — Core Track"

    return {
        "title": title,
        "weeks": out_weeks,
        "personalization_notes": notes,
        "focus_areas": focus_areas or (subtopics[:3]),
    }


def _validate(payload: dict[str, Any], weeks: int, topic: str) -> dict[str, Any] | None:
    raw_weeks = payload.get("weeks")
    if not isinstance(raw_weeks, list) or len(raw_weeks) != weeks:
        return None

    out: list[dict[str, Any]] = []
    for i, w in enumerate(raw_weeks, start=1):
        if not isinstance(w, dict):
            return None
        topics = w.get("topics")
        if not isinstance(topics, list) or not topics:
            return None

        norm_topics = []
        for t in topics:
            if not isinstance(t, dict) or not t.get("name"):
                return None
            difficulty = str(t.get("difficulty", "medium")).lower()
            if difficulty not in ("easy", "medium", "hard"):
                difficulty = "medium"
            norm_topics.append(
                {
                    "name": str(t["name"]),
                    "subtopic": str(t.get("subtopic") or t["name"]),
                    "difficulty": difficulty,
                    "estimated_hours": float(t.get("estimated_hours") or 4),
                    "why_this_matters": str(t.get("why_this_matters", "")).strip()
                    or "Part of your personalised plan.",
                    "resources": [str(r) for r in (t.get("resources") or [])][:3]
                    or ["Practice questions", "Reading notes"],
                }
            )

        out.append(
            {
                "week": int(w.get("week") or i),
                "title": str(w.get("title") or f"Week {i}"),
                "focus": str(w.get("focus") or ", ".join(t["name"] for t in norm_topics)),
                "topics": norm_topics,
                "practice_target": int(w.get("practice_target") or 12),
                "milestone": str(w.get("milestone") or "Complete the week's practice set."),
            }
        )

    return {
        "title": str(payload.get("title") or f"{display_name(topic)} Plan"),
        "weeks": out,
        "personalization_notes": [
            str(n) for n in (payload.get("personalization_notes") or [])
        ][:6]
        or ["Personalised from your assessment and goal."],
        "focus_areas": [str(f) for f in (payload.get("focus_areas") or [])][:6],
    }


async def generate_roadmap(
    *,
    name: str,
    topic: str,
    level: str,
    goal: str,
    hours_per_week: float,
    weeks: int,
    score: float | None,
    strong: list[str],
    weak: list[str],
) -> tuple[dict[str, Any], str]:
    """Return (roadmap_dict, ai_mode)."""
    payload = await generate_json_or_none(
        prompts.ROADMAP_SYSTEM,
        prompts.roadmap_prompt(
            name=name,
            topic=topic,
            level=level,
            goal=goal,
            hours_per_week=hours_per_week,
            target_duration=weeks,
            score_pct=score,
            strong=strong,
            weak=weak,
        ),
    )

    validated = _validate(payload, weeks, topic) if payload else None
    if validated:
        return validated, "live"

    if settings.ai_enabled:
        logger.info("Roadmap generation fell back to the deterministic planner.")
    return (
        _build_plan(
            topic=topic,
            level=level,
            goal=goal,
            weeks=weeks,
            hours_per_week=hours_per_week,
            score=score,
            strong=strong,
            weak=weak,
        ),
        "offline",
    )
