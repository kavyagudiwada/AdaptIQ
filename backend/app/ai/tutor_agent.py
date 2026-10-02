"""Tutor agent: produces level-appropriate, context-aware explanations.

Never behaves like a generic chatbot: the learner profile, weak topics, recent
scores and roadmap position are all injected into the prompt, and the offline
path applies the same adaptation rules.
"""

from __future__ import annotations

import logging
from typing import Any

from app.ai import prompts
from app.ai.demo_content import TUTOR_BANK
from app.ai.llm_service import generate_json_or_none
from app.core.config import settings
from app.utils.curriculum import display_name, subtopics_for

logger = logging.getLogger(__name__)

# Word budget per level keeps explanations appropriately sized.
DEPTH = {
    "beginner": {
        "explanation": "2-3 short paragraphs, everyday language, one analogy",
        "example": "one very concrete everyday example, no code",
        "points": 3,
        "mistakes": 2,
    },
    "intermediate": {
        "explanation": "3-4 paragraphs, technical terms, mention the mechanism",
        "example": "one worked practical example, short code snippet is welcome",
        "points": 4,
        "mistakes": 3,
    },
    "advanced": {
        "explanation": "4-5 paragraphs, include the mathematics and assumptions",
        "example": "one advanced or production-scale example, include trade-offs",
        "points": 5,
        "mistakes": 3,
    },
}

_FOLLOW_UPS = {
    "beginner": "Can you explain in one sentence why that matters in a real project?",
    "intermediate": "Would you use this approach for a tabular dataset of 100k rows? Why?",
    "advanced": "What breaks down with this approach at scale, and what would you use instead?",
}


def _normalise(payload: dict[str, Any], level: str) -> dict[str, Any] | None:
    explanation = str(payload.get("explanation", "")).strip()
    example = str(payload.get("example", "")).strip()
    if not explanation:
        return None

    depth = DEPTH.get(level, DEPTH["beginner"])
    points = [str(p).strip() for p in (payload.get("key_points") or []) if str(p).strip()]
    mistakes = [
        str(m).strip() for m in (payload.get("common_mistakes") or []) if str(m).strip()
    ]

    return {
        "explanation": explanation,
        "example": example or "See the explanation above for a worked example.",
        "key_points": points[: depth["points"]] or ["Review the explanation above."],
        "common_mistakes": mistakes[: depth["mistakes"]]
        or ["Skipping the fundamentals and jumping to advanced usage."],
        "follow_up_question": str(payload.get("follow_up_question", "")).strip()
        or _FOLLOW_UPS.get(level, _FOLLOW_UPS["beginner"]),
    }


def _bank_body(
    *,
    banked: dict[str, Any],
    topic: str,
    subtopic: str,
    level: str,
    goal: str,
    strong: list[str],
    weak: list[str],
    learner_question: str,
) -> dict[str, Any]:
    """Build an offline tutor response from the curated per-topic bank.

    Personalisation is layered on top of the bank: weak/strong framing, the
    learner's goal, and a direct answer to their specific question. Bank content
    is written at a solid default depth; the learner's level only picks the
    difficulty label so the UI badge stays honest.
    """
    is_weak = subtopic.lower() in {w.lower() for w in weak}
    is_strong = subtopic.lower() in {s.lower() for s in strong}
    topic_name = display_name(topic)

    gap_note = (
        "This is one of your weak areas, so take it slowly and re-run the example yourself."
        if is_weak
        else (
            "You already scored well here, so treat this as a refresher that focuses on the details you may have glossed over."
            if is_strong
            else "This is new ground for you, so the explanation deliberately starts from first principles."
        )
    )
    goal_note = {
        "placement": "Interviewers ask about this often, so it is worth memorising cleanly.",
        "interview": "This is a favourite interview question - practise saying it out loud.",
        "academic": "This maps directly to the standard syllabus, so focus on the precise definition.",
        "project": "You will use this in a project, so keep the implementation detail in mind.",
        "general": "Build the intuition first, then formalise it.",
    }[goal]

    answer = ""
    if learner_question:
        answer = (
            f"\n\n**On your question** — {learner_question.strip()}.\n"
            f"Applied to **{subtopic}**: run the worked example above with your own numbers and "
            f"check the result against the formula by hand once. If it does not match, either the "
            f"assumptions (e.g. independence or scaling) are violated or a step is glossing over a "
            f"term you can pinpoint — that is exactly the place to stop and ask again."
        )

    return {
        "topic": subtopic,
        "explanation": (
            f"{banked['explanation']}\n\n**How this applies to you.** {gap_note} {goal_note}{answer}"
        ),
        "example": banked["example"],
        "key_points": list(banked["key_points"]),
        "common_mistakes": list(banked["common_mistakes"]),
        "follow_up_question": banked.get("follow_up_question") or _FOLLOW_UPS.get(
            level, _FOLLOW_UPS["beginner"]
        ),
        "difficulty": {"beginner": "easy", "intermediate": "medium"}.get(
            level, "hard"
        ),
        "personalized_note": f"{gap_note} {goal_note}",
    }


def _demo_body(
    *,
    name: str,
    topic: str,
    subtopic: str,
    level: str,
    goal: str,
    strong: list[str],
    weak: list[str],
    learner_question: str,
) -> dict[str, Any]:
    """Offline explanation that still varies meaningfully by learner."""
    banked = TUTOR_BANK.get(subtopic.strip().lower())
    if banked is not None:
        return _bank_body(
            banked=banked,
            topic=topic,
            subtopic=subtopic,
            level=level,
            goal=goal,
            strong=strong,
            weak=weak,
            learner_question=learner_question,
        )

    is_weak = subtopic.lower() in {w.lower() for w in weak}
    is_strong = subtopic.lower() in {s.lower() for s in strong}
    topic_name = display_name(topic)
    gap_note = (
        f"This is one of your weak areas, so take it slowly and re-run the example yourself."
        if is_weak
        else (
            f"You already scored well here, so this is a refresher that focuses on the details you may have glossed over."
            if is_strong
            else "This is new ground for you, so the explanation starts from first principles."
        )
    )
    goal_note = {
        "placement": "Interviewers ask about this often, so it is worth memorising cleanly.",
        "interview": "This is a favourite interview question - practise saying it out loud.",
        "academic": "This maps directly to the standard syllabus, so focus on the precise definition.",
        "project": "You will use this in a project, so keep the implementation detail in mind.",
        "general": "Build the intuition first, then formalise it.",
    }[goal]

    if level == "beginner":
        explanation = (
            f"**{subtopic}** is one of the building blocks of {topic_name}. "
            f"Think of {topic_name} as learning to make decisions from examples, and {subtopic} "
            f"is the part that helps you make sense of those examples.\n\n"
            f"Here is the simple version: {subtopic} helps the computer spot a pattern in the data you give it, "
            f"and then use that pattern to guess what will happen next time. "
            f"A good analogy is a shopkeeper who has seen thousands of customers. They do not memorise every person, "
            f"but they notice patterns — tall people buy this, people on Fridays buy that — and predict accordingly.\n\n"
            f"The key idea to hold onto: you feed in data, the algorithm finds the pattern for you, "
            f"and you check whether the pattern is actually useful on data it has not seen before.\n\n"
            f"{gap_note}"
        )
        example = (
            f"Imagine you want to predict whether an email is spam. You already know "
            f"{subtopic}, so you can describe what makes spam different — certain words, "
            f"too many links, an urgent tone. You show the computer a few thousand labelled emails "
            f"and it learns that pattern on its own. When a new email arrives, it applies what it learned. "
            f"Now imagine the very first email it ever sees mentions 'free money' — same pattern, same prediction. "
            f"That is {subtopic} in action with no mathematics at all."
        )
        key_points = [
            f"{subtopic} is a step inside the wider {topic_name} workflow.",
            "It works by finding patterns in examples you already have.",
            "We always test on unseen data to check the pattern is real, not memorised.",
        ]
        mistakes = [
            "Skipping straight to code before understanding what the step is for.",
            "Judging the method by how well it fits the data it was trained on.",
        ]
        difficulty = "easy"

    elif level == "intermediate":
        explanation = (
            f"### {subtopic} in {topic_name}\n\n"
            f"{subtopic} sits between raw data and a usable model. Mechanically, it takes "
            f"features X and a target y and learns a function f that maps one to the other. "
            f"The key distinction is what happens to the parameters during fitting: in {subtopic} "
            f"the objective is minimised directly over that parameter space rather than approximated.\n\n"
            f"Three things to keep in mind:\n"
            f"- **Assumptions**: it performs best when features are on comparable scales and roughly independent.\n"
            f"- **Diagnostics**: check residuals (for regression) or the confusion matrix (for classification) before trusting it.\n"
            f"- **Capacity control**: depth, regularisation strength or K determine how complex the fit is allowed to become.\n\n"
            f"{gap_note} {goal_note}"
        )
        example = (
            f"Worked example: predicting house prices.\n"
            f"```python\n"
            f"X = df[['area', 'rooms', 'location_score']]\n"
            f"y = df['price']\n\n"
            f"from sklearn.model_selection import train_test_split\n"
            f"from sklearn.pipeline import make_pipeline\n"
            f"from sklearn.preprocessing import StandardScaler\n\n"
            f"X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)\n"
            f"model = make_pipeline(StandardScaler(), LinearRegression())\n"
            f"model.fit(X_tr, y_tr)\n"
            f"print(model.score(X_te, y_te))  # R^2 on unseen data\n"
            f"```\n"
            f"Scaling matters because `area` is measured in square feet while `rooms` is a small integer — "
            f"without the scaler the larger-magnitude feature dominates the fit."
        )
        key_points = [
            f"{subtopic} optimises a parameterised objective over features X to predict target y.",
            "Feature scaling and assumption checks materially change the result.",
            f"Validate on a held-out split, not the training set — that is how {subtopic} is judged.",
        ]
        mistakes = [
            "Reporting training accuracy as if it were generalisation performance.",
            "Fitting preprocessing on the full dataset instead of only the training fold.",
            "Ignoring class imbalance when choosing an evaluation metric.",
        ]
        difficulty = "medium"

    else:
        explanation = (
            f"## {subtopic} — technical treatment\n\n"
            f"At the level of formulation, {subtopic} optimises\n\n"
            f"$$\\theta^* = \\arg\\min_\\theta \\; \\mathcal{{L}}(\\theta; X, y) + \\lambda \\Omega(\\theta)$$\n\n"
            f"where $\\mathcal{{L}}$ is the empirical loss, $\\Omega$ a regulariser, and $\\lambda$ the "
            f"regularisation strength traded off against fit.\n\n"
            f"**Statistical properties.** Consistency requires the hypothesis class to be "
            f"well-specified or the loss to be quasi-convex; otherwise the estimator converges to a "
            f"projection onto the reachable set rather than the true minimiser.\n\n"
            f"**Complexity.** Compute is $O(n \\cdot d \\cdot k)$ for $n$ samples, $d$ dimensions and "
            f"$k$ iterations, with memory typically $O(n \\cdot d)$.\n\n"
            f"**Failure modes.** Distribution shift between train and serve violates the i.i.d. assumption; "
            f"catastrophic forgetting occurs when updates are replayed non-stationarily; and leakage through "
            f"preprocessing fitted on the full dataset inflates generalisation estimates.\n\n"
            f"{gap_note} {goal_note}"
        )
        example = (
            "Production-scale scenario: streaming demand forecasting where labels arrive with a 14-day lag.\n"
            "The naive approach regresses on raw lags and silently leaks, because the rolling-window feature "
            "is computed over the full series before splitting. The correct pipeline fits the transformer on "
            "the training window only:\n"
            "```python\n"
            "scaler = StandardScaler().fit(X_train)      # fitted on train only\n"
            "X_train_t = scaler.transform(X_train)\n"
            "X_test_t  = scaler.transform(X_test)        # same transform reused\n"
            "```\n"
            "Latency then becomes the binding constraint: batch scoring at 50 ms/request caps throughput "
            "near 20 req/s, which motivates switching to an incremental update rule."
        )
        key_points = [
            f"The objective couples data fit $\\mathcal{{L}}$ with a regulariser $\\lambda\\Omega(\\theta)$.",
            "Assumptions and failure modes matter more than hyperparameter defaults at this level.",
            "Any preprocessing must be fitted inside the training fold to avoid leakage.",
            "Evaluate stability across seeds, not a single lucky split.",
        ]
        mistakes = [
            "Reporting a single-split score with no variance estimate.",
            "Fitting scalers or encoders on the full dataset before splitting.",
            "Ignoring label lag in streaming setups, which leaks future information.",
        ]
        difficulty = "hard"

    if learner_question:
        explanation += (
            f"\n\n**On your question** — {learner_question} — the short answer is that it "
            f"depends on the data size and the cost of errors, so start with the simplest version "
            f"of {subtopic} that answers the question, then optimise only if measurement shows it matters."
        )

    return {
        "topic": subtopic,
        "explanation": explanation,
        "example": example,
        "key_points": key_points,
        "common_mistakes": mistakes,
        "follow_up_question": _FOLLOW_UPS.get(level, _FOLLOW_UPS["beginner"]),
        "difficulty": difficulty,
        "personalized_note": f"{gap_note} {goal_note}",
    }


async def explain(
    *,
    name: str,
    topic: str,
    subtopic: str,
    level: str,
    goal: str,
    estimated_level: str | None,
    strong: list[str],
    weak: list[str],
    recent_scores: str,
    learner_question: str,
    roadmap_week: int | None,
) -> tuple[dict[str, Any], str]:
    """Return (tutor_response, ai_mode)."""
    if not subtopic:
        subtopic = subtopics_for(topic)[0]

    payload = await generate_json_or_none(
        prompts.TUTOR_SYSTEM,
        prompts.tutor_prompt(
            name=name,
            topic=topic,
            subtopic=subtopic,
            level=level,
            goal=goal,
            estimated_level=estimated_level,
            strong=strong,
            weak=weak,
            recent_scores=recent_scores,
            learner_question=learner_question,
            roadmap_week=roadmap_week,
        ),
    )

    if payload:
        body = _normalise(payload, level)
        if body:
            return (
                {
                    "topic": subtopic,
                    **body,
                    "difficulty": level if level in ("easy", "medium", "hard") else "medium",
                    "personalized_note": _personalized_note(
                        level, strong, weak, goal
                    ),
                },
                "live",
            )

    if settings.ai_enabled:
        logger.info("Tutor explanation fell back to offline content.")
    return (
        _demo_body(
            name=name,
            topic=topic,
            subtopic=subtopic,
            level=level,
            goal=goal,
            strong=strong,
            weak=weak,
            learner_question=learner_question,
        ),
        "offline",
    )


def _personalized_note(level: str, strong: list[str], weak: list[str], goal: str) -> str:
    bits = []
    if weak:
        bits.append(f"Targeting your weak area: {', '.join(weak[:2])}.")
    if strong:
        bits.append(f"Building on what you already know: {', '.join(strong[:2])}.")
    bits.append(f"Written at {level} depth.")
    bits.append(
        {
            "placement": "Framed for placement preparation.",
            "interview": "Framed for interview preparation.",
            "academic": "Framed for syllabus coverage.",
            "project": "Framed for project building.",
            "general": "Framed for steady self-study.",
        }[goal]
    )
    return " ".join(bits)
