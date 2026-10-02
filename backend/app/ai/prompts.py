"""Dedicated prompt templates.

Every prompt is built from real learner context (level, goal, weak topics,
recent scores) so the AI output is personalised rather than generic.
"""

from __future__ import annotations

from typing import Any

from app.utils.curriculum import display_name, subtopics_for

LEVEL_STYLE = {
    "beginner": (
        "Use simple everyday language, relatable analogies and concrete real-world "
        "examples. Avoid jargon, avoid heavy mathematics, and spell out every term "
        "the first time you use it."
    ),
    "intermediate": (
        "Use precise technical language with practical detail: include the actual "
        "method names, the formulas where they matter, and short code or worked "
        "examples a practitioner would recognise."
    ),
    "advanced": (
        "Go deep: include mathematical formulation, implementation-level detail, "
        "assumptions, edge cases, limitations, and how the idea behaves in real "
        "production systems."
    ),
}

GOAL_FRAMING = {
    "academic": "Frame content around syllabus coverage, exam-style questions and clear proofs or definitions.",
    "placement": "Frame content around what interviewers ask: practical debugging, common pitfalls, and company-style case problems.",
    "interview": "Frame content as interview preparation: rapid-fire conceptual questions, whiteboard reasoning, and what to say aloud.",
    "project": "Frame content around building things: concrete implementation steps, library choices, and end-to-end project steps.",
    "general": "Frame content as clear, balanced self-study with a steady practice rhythm.",
}


def learner_block(
    *,
    name: str,
    topic: str,
    level: str,
    goal: str,
    hours_per_week: float,
    target_duration: int,
    estimated_level: str | None = None,
) -> str:
    """Shared learner context injected into every prompt."""
    lines = [
        f"Name: {name}",
        f"Topic: {display_name(topic)}",
        f"Self-reported level: {level}",
        f"Learning goal: {goal}",
        f"Study budget: {hours_per_week} hours/week for {target_duration} weeks",
    ]
    if estimated_level:
        lines.append(f"AI-estimated level after assessment: {estimated_level}")
    lines.append(f"Style guidance: {LEVEL_STYLE.get(level, LEVEL_STYLE['beginner'])}")
    lines.append(f"Framing: {GOAL_FRAMING.get(goal, GOAL_FRAMING['general'])}")
    return "\n".join(lines)


def score_block(
    *,
    score_pct: float | None = None,
    strong: list[str] | None = None,
    weak: list[str] | None = None,
    recent: str | None = None,
) -> str:
    parts: list[str] = []
    if score_pct is not None:
        parts.append(f"Assessment score: {score_pct}%")
    if strong:
        parts.append(f"Strong topics: {', '.join(strong)}")
    if weak:
        parts.append(f"Weak topics: {', '.join(weak)}")
    if recent:
        parts.append(recent)
    return "\n".join(parts) if parts else "No performance data yet."


# ---------------------------------------------------------------------------
# 1. Assessment generation
# ---------------------------------------------------------------------------

ASSESSMENT_GENERATION_SYSTEM = """You are an expert technical assessor building a short \
diagnostic quiz for a learner.

Return STRICT JSON only, with this exact shape:
{
  "questions": [
    {
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correct_index": 0,
      "subtopic": "string",
      "difficulty": "easy" | "medium" | "hard"
    }
  ]
}

Rules:
- Produce exactly the number of questions requested, with exactly 4 options each.
- Spread the questions across DIFFERENT subtopics so weak areas are detectable.
- correct_index must be the 0-based index of the right option.
- Distractors must be plausible and clearly wrong, never silly.
- Difficulty must match the learner's level: a beginner gets mostly easy, an advanced learner gets mostly medium and hard.
- Use only subtopics from the provided list.
- No markdown, no commentary, JSON only."""


def assessment_generation_prompt(
    *, count: int, topic: str, level: str, goal: str, subtopics: list[str]
) -> str:
    return (
        f"Create a {count}-question diagnostic assessment.\n\n"
        f"Topic: {display_name(topic)}\n"
        f"Learner level: {level}\n"
        f"Learning goal: {goal}\n"
        f"Allowed subtopics (spread questions across these):\n"
        + "\n".join(f"- {s}" for s in subtopics)
        + "\n\n"
        f"Difficulty mix for a {level} learner: "
        + {
            "beginner": "3 easy, 2 medium",
            "intermediate": "2 easy, 2 medium, 1 hard",
            "advanced": "1 easy, 2 medium, 2 hard",
        }.get(level, "2 easy, 2 medium, 1 hard")
    )


# ---------------------------------------------------------------------------
# 2. Assessment analysis
# ---------------------------------------------------------------------------

ASSESSMENT_ANALYSIS_SYSTEM = """You are an expert learning analyst reviewing a diagnostic quiz result.

Return STRICT JSON only:
{
  "estimated_level": "beginner" | "intermediate" | "advanced",
  "strong_topics": ["string"],
  "weak_topics": ["string"],
  "feedback": "2-3 encouraging sentences addressed directly to the learner"
}

Rules:
- Use ONLY subtopics that actually appeared in the quiz.
- strong_topics = subtopics answered fully correctly.
- weak_topics = subtopics with any mistake.
- Be honest but encouraging. Address the learner by name.
- No markdown, JSON only."""


def assessment_analysis_prompt(
    *,
    name: str,
    level: str,
    topic: str,
    score_pct: float,
    per_subtopic: list[dict[str, Any]],
) -> str:
    rows = "\n".join(
        f"- {r['subtopic']}: {r['correct']}/{r['total']} correct ({r['percentage']}%)"
        for r in per_subtopic
    )
    return (
        f"{learner_block(name=name, topic=topic, level=level, goal='general', hours_per_week=0, target_duration=0)}\n\n"
        f"Overall score: {score_pct}%\n\n"
        f"Per-subtopic breakdown:\n{rows}\n\n"
        "Analyse this and decide the learner's true level plus their strong and weak areas."
    )


# ---------------------------------------------------------------------------
# 3. Roadmap generation
# ---------------------------------------------------------------------------

ROADMAP_SYSTEM = """You are an expert curriculum designer building a personalised learning roadmap.

Return STRICT JSON only:
{
  "title": "string",
  "weeks": [
    {
      "week": 1,
      "title": "string",
      "focus": "string",
      "topics": [
        {
          "name": "string",
          "subtopic": "string",
          "difficulty": "easy" | "medium" | "hard",
          "estimated_hours": 4,
          "why_this_matters": "one sentence",
          "resources": ["string", "string"]
        }
      ],
      "practice_target": 10,
      "milestone": "string"
    }
  ],
  "personalization_notes": ["string"],
  "focus_areas": ["string"]
}

PERSONALISATION RULES (this is the whole point):
- A learner who scored HIGH skips basic material and moves to advanced, application-heavy topics fast.
- A learner who scored LOW gets fundamentals first, more examples, extra practice, and a longer runway on basics.
- Weak topics must appear EARLY in the roadmap and get more practice_target than strong topics.
- Strong topics should be brief review only, never re-taught from scratch.
- The number of weeks MUST equal the learner's target duration. The total estimated hours per week must respect their stated hours_per_week.
- Topics must come from the allowed subtopic list for this topic.
- No markdown, JSON only."""


def roadmap_prompt(
    *,
    name: str,
    topic: str,
    level: str,
    goal: str,
    hours_per_week: float,
    target_duration: int,
    score_pct: float | None,
    strong: list[str],
    weak: list[str],
) -> str:
    context = learner_block(
        name=name,
        topic=topic,
        level=level,
        goal=goal,
        hours_per_week=hours_per_week,
        target_duration=target_duration,
    )
    performance = score_block(score_pct=score_pct, strong=strong, weak=weak)

    if score_pct is None:
        pace = (
            "No assessment score yet. Start with fundamentals and keep the pace moderate."
        )
    elif score_pct >= 75:
        pace = (
            "This learner scored very high. COMPRESS the basics: cover them quickly as "
            "revision only, and spend the roadmap on advanced and application topics."
        )
    elif score_pct >= 50:
        pace = (
            "This learner has a moderate grasp. Keep the core sequence, but skip the "
            "most elementary steps and add application practice."
        )
    else:
        pace = (
            "This learner scored low. SLOW DOWN: add fundamentals, add worked examples, "
            "increase practice targets, and repeat the weak subtopics later for reinforcement."
        )

    allowed = subtopics_for(topic)
    return (
        f"{context}\n\n{performance}\n\n{pace}\n\n"
        f"Allowed subtopics for {display_name(topic)}:\n"
        + "\n".join(f"- {s}" for s in allowed)
        + f"\n\nProduce exactly {target_duration} weeks."
    )


# ---------------------------------------------------------------------------
# 4. Tutor explanation
# ---------------------------------------------------------------------------

TUTOR_SYSTEM = """You are a personal AI tutor. You are NOT a generic chatbot: you must adapt to the specific learner described.

Return STRICT JSON only:
{
  "explanation": "markdown string",
  "example": "markdown string with a concrete worked example",
  "key_points": ["string", "string", "string"],
  "common_mistakes": ["string", "string"],
  "follow_up_question": "one probing question"
}

Rules:
- Match the learner's level exactly using the style guidance provided.
- Anchor the explanation in the learner's weak topics and recent scores.
- Keep explanation focused: 150-300 words. No filler.
- The example must be concrete and runnable-looking, not abstract.
- If the learner is a beginner, use analogies and everyday language.
- If advanced, include mathematics, assumptions and limitations.
- Write every formula in LaTeX math delimiters so it renders properly: inline
  math as $...$ and a standalone equation on its own line as $$...$$ (e.g.
  "The slope is $\\hat{\\beta} = \\frac{\\text{cov}(x, y)}{\\text{var}(x)}$"). Do NOT leave
  maths as plain prose like "x squared plus y".
- Address the learner directly and reference their goal.
- No markdown outside the JSON, JSON only."""


def tutor_prompt(
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
) -> str:
    focus = f"Week {roadmap_week} of their roadmap" if roadmap_week else "their roadmap"
    return (
        f"{learner_block(name=name, topic=topic, level=level, goal=goal, hours_per_week=0, target_duration=0, estimated_level=estimated_level)}\n\n"
        f"Current roadmap position: {focus}\n"
        f"{score_block(strong=strong, weak=weak, recent=recent_scores)}\n\n"
        f"Topic to explain: {subtopic}\n"
        f"Their own question: {learner_question or 'No specific question - give the core explanation.'}\n\n"
        "Explain this so it fits THIS learner, not a generic reader."
    )


# ---------------------------------------------------------------------------
# 5. Quiz generation
# ---------------------------------------------------------------------------

QUIZ_SYSTEM = """You are an expert quiz generator producing adaptive practice.

Return STRICT JSON only:
{
  "questions": [
    {
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correct_index": 0,
      "subtopic": "string",
      "difficulty": "easy" | "medium" | "hard",
      "explanation": "one sentence explaining the correct answer"
    }
  ]
}

Rules:
- Produce exactly the number of questions requested, all at the difficulty level named in the request.
- ALL questions must be about the requested topic/subtopic.
- easy = definitions and recall. medium = applied reasoning. hard = scenario, analysis, trade-offs, multi-step thinking.
- Distractors must be plausible and clearly wrong.
- Every question needs a helpful explanation shown after answering.
- No markdown, JSON only."""


def quiz_prompt(
    *, count: int, topic: str, subtopic: str, difficulty: str, level: str, weak: list[str]
) -> str:
    return (
        f"Generate {count} practice questions.\n"
        f"Topic: {display_name(topic)}\n"
        f"Subtopic: {subtopic}\n"
        f"Difficulty: {difficulty}\n"
        f"Learner level: {level}\n"
        f"Their weak areas: {', '.join(weak) if weak else 'none recorded'}\n\n"
        "Make the hard questions genuinely require reasoning, not just recall of harder facts."
    )


# ---------------------------------------------------------------------------
# 6. Performance analysis
# ---------------------------------------------------------------------------

PERFORMANCE_SYSTEM = """You are an expert learning coach reviewing practice history.

Return STRICT JSON only:
{
  "recommended_next_topic": "string",
  "recommendation_reason": "2-3 sentences naming the specific score or topic that drove the decision",
  "current_topic": "string"
}

Rules:
- Base the recommendation on the weakest topic with enough evidence.
- If everything is strong, recommend a more advanced topic from the allowed list.
- Be specific and reference actual numbers.
- No markdown, JSON only."""


def performance_prompt(
    *,
    name: str,
    topic: str,
    level: str,
    goal: str,
    allowed: list[str],
    topic_scores: list[dict[str, Any]],
) -> str:
    rows = "\n".join(
        f"- {r['topic']}: latest score {r['last_score']}%, mastery {r['mastery_level']}"
        for r in topic_scores
    ) or "No topic scores recorded yet."
    return (
        f"{learner_block(name=name, topic=topic, level=level, goal=goal, hours_per_week=0, target_duration=0)}\n\n"
        f"Topic-by-topic performance:\n{rows}\n\n"
        f"Allowed topics: {', '.join(allowed)}\n\n"
        "Decide what this learner should do next and justify it with their actual numbers."
    )


# ---------------------------------------------------------------------------
# 7. Misconception diagnosis
# ---------------------------------------------------------------------------

MISCONCEPTION_SYSTEM = """You are a diagnostic learning analyst. For every WRONG answer, \
name the exact misconception the learner's chosen option reveals, then give ONE concrete \
fix they should do next.

Return STRICT JSON only:
{
  "misconceptions": [
    {
      "question_id": "string",
      "misconception": "the specific flawed mental model, one sentence",
      "fix": "one actionable next step, addressed to the learner"
    }
  ]
}

Rules:
- Only include questions the learner answered WRONG.
- The misconception must be a plausible, specific reason a student would pick \
that wrong option (e.g. a reversed rule, a dropped step, confusing two adjacent concepts).
- Never just say "you guessed". Name the idea behind the error.
- A "fix" is a concrete action (re-read the linked concept, rework a problem, \
check a specific step), not encouragement alone.
- No markdown, JSON only."""


def misconception_prompt(
    *,
    topic: str,
    subtopic: str,
    level: str,
    wrong_questions: list[dict[str, Any]],
) -> str:
    rows = "\n".join(
        (
            f"- Question \"{q['question']}\"\n"
            f"  Options: {'; '.join(q['options'])}\n"
            f"  Learner chose: {q['options'][q['selected_index']]}\n"
            f"  Correct answer: {q['options'][q['correct_index']]}\n"
            f"  Explanation: {q['explanation']}"
        )
        for q in wrong_questions
    )
    return (
        f"Topic: {display_name(topic)}\n"
        f"Subtopic: {subtopic}\n"
        f"Learner level: {level}\n\n"
        f"Wrong answers to diagnose:\n{rows}\n\n"
        "Diagnose each one. Use ONLY the question_id values given."
    )


# ---------------------------------------------------------------------------
# 8. Confidence calibration
# ---------------------------------------------------------------------------

CALIBRATION_SYSTEM = """You are a metacognitive coach. The learner rated how sure they \
were of each answer (1 = guessing, 5 = very sure). We compared that to their actual \
accuracy and computed a calibration gap (positive = overconfident, negative = underconfident).

Return STRICT JSON only:
{
  "feedback": "2-3 sentences explaining the gap and how to calibrate, addressed to the learner"
}

Rules:
- Reference the actual numbers: their average confidence vs their score.
- Be specific about the behaviour to change (slow down, trust more, attempt first then check).
- Encourage, do not scold. No markdown, JSON only."""


def calibration_prompt(
    *,
    name: str,
    level: str,
    topic: str,
    confidence_avg: float,
    accuracy: float,
    gap: float,
    answered_count: int,
) -> str:
    direction = (
        "they were overconfident"
        if gap > 5
        else "they were underconfident"
        if gap < -5
        else "their confidence closely matched their results"
    )
    return (
        f"Learner: {name} (level {level}, practising {display_name(topic)})\n\n"
        f"Average self-confidence: {confidence_avg:.0f}%\n"
        f"Actual accuracy: {accuracy:.0f}%\n"
        f"Calibration gap: {gap:+.0f} points ({direction})\n"
        f"Rated questions: {answered_count}\n\n"
        "Give them calibration coaching based on their actual numbers."
    )
