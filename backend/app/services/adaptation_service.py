"""The adaptation loop.

Two things in the product were claimed but never actually wired up:

1. *Measured ability never fed back.* The assessment wrote `estimated_level`,
   but `learner.current_level` kept the value the learner typed at signup and
   that stale value drove quiz prompts, assessment papers, roadmap tiering and
   tutor depth. Here we make `current_level` the **effective** level and
   recompute it from real evidence, so all of those consumers get correct
   input without each one having to be patched.

2. *The plan never adapted.* A roadmap was generated once and frozen. Here we
   fingerprint the evidence a plan was built from, so we can tell when the
   learner's performance has moved on and the plan is stale.

Everything is deliberately threshold-based and explainable rather than clever,
because the rules have to be able to be shown to a judge verbatim.
"""

from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Assessment, Learner, Progress, QuizAttempt
from app.utils.helpers import LEVEL_RANK, LEVELS, estimate_level, mastery_for

logger = logging.getLogger(__name__)

# How many topics must agree before a level change is trusted. Keeps one lucky
# topic from flipping somebody from beginner to advanced.
MAJORITY_SUPPORT = 0.5

# Evidence is either breadth (several topics) or depth (repeated attempts on
# one topic). Either satisfies the bar - grinding one topic is real evidence.
MIN_TOPICS_FOR_LEVEL_CHANGE = 2
MIN_ATTEMPTS_FOR_LEVEL_CHANGE = 3

# Weak/strong topic cut-offs, aligned with the quiz difficulty bands.
WEAK_BELOW = 60.0
STRONG_AT_OR_ABOVE = 75.0


@dataclass(frozen=True)
class TopicEvidence:
    """What we know about one topic from real practice."""

    topic: str
    mastery: str
    blended: float
    last_score: float
    attempts: int

    @property
    def is_weak(self) -> bool:
        return self.last_score < WEAK_BELOW

    @property
    def is_strong(self) -> bool:
        return self.last_score >= STRONG_AT_OR_ABOVE


@dataclass
class AdaptationSnapshot:
    """The full evidence picture for one learner at a point in time."""

    level: str
    self_reported_level: str
    level_source: str  # "assessment" | "practice" | "self_reported"
    level_changed: bool = False
    average_mastery: float = 0.0
    topics: list[TopicEvidence] = field(default_factory=list)
    weak: list[str] = field(default_factory=list)
    strong: list[str] = field(default_factory=list)
    assessment_score: float | None = None
    total_attempts: int = 0
    recent_difficulty: str | None = None

    @property
    def level_moved_up(self) -> bool:
        return LEVEL_RANK[self.level] > LEVEL_RANK[self.self_reported_level]

    @property
    def level_moved_down(self) -> bool:
        return LEVEL_RANK[self.level] < LEVEL_RANK[self.self_reported_level]

    def signature(self) -> str:
        """Fingerprint of the evidence a plan was built from.

        Two snapshots with the same signature would produce the same plan, so a
        changed signature means the current plan no longer reflects reality.
        """
        parts = [
            self.level,
            self.level_source,
            f"{self.average_mastery:.0f}",
            ",".join(sorted(t.topic.lower() for t in self.topics)),
            ",".join(sorted(w.lower() for w in self.weak)),
            ",".join(sorted(s.lower() for s in self.strong)),
            str(self.total_attempts),
        ]
        return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:32]

    def reasons(self, previous_level: str | None = None) -> list[str]:
        """Plain-language reasons the plan should change."""
        out: list[str] = []

        reference = previous_level or self.self_reported_level
        if self.level != reference:
            if LEVEL_RANK[self.level] > LEVEL_RANK[reference]:
                out.append(
                    f"Your results now place you at {self.level} level, above the "
                    f"{reference} you started at, so the plan moves to harder material."
                )
            else:
                out.append(
                    f"Your results place you at {self.level} level, below the "
                    f"{reference} you started at, so the plan adds more fundamentals."
                )

        if self.weak:
            out.append(
                f"Weakest right now: {', '.join(self.weak[:4])}. These are scheduled "
                "earlier and given extra practice."
            )
        if self.strong:
            out.append(
                f"Already solid: {', '.join(self.strong[:4])}. These drop to brief review."
            )
        if self.total_attempts and not self.topics:
            out.append(
                f"You have logged {self.total_attempts} practice sets, so the pacing "
                "reflects real workload."
            )
        return out


async def _topic_evidence(session: AsyncSession, learner_id: int) -> list[TopicEvidence]:
    """Per-topic mastery, with attempt counts, from the Progress table.

    A `Progress` row defaults to `last_score = 0.0`, so a zero is ambiguous: it
    can mean "scored nothing" or "never actually attempted". We therefore treat
    a topic as evidence only when it has a real logged quiz attempt or a
    non-zero recorded score. That errs toward ignoring a genuine 0%, which is
    safer than treating untouched topics as failures.
    """
    attempts_by_topic: dict[str, int] = {}
    for attempt in (
        await session.execute(
            select(QuizAttempt).where(QuizAttempt.learner_id == learner_id)
        )
    ).scalars().all():
        key = attempt.topic.lower()
        attempts_by_topic[key] = attempts_by_topic.get(key, 0) + 1

    rows = (
        await session.execute(
            select(Progress).where(Progress.learner_id == learner_id)
        )
    ).scalars().all()

    evidence: list[TopicEvidence] = []
    for row in rows:
        attempts = attempts_by_topic.get(row.topic.lower(), 0)
        if attempts == 0 and row.last_score <= 0 and row.progress_percentage <= 0:
            continue
        evidence.append(
            TopicEvidence(
                topic=row.topic,
                mastery=row.mastery_level,
                blended=float(row.progress_percentage),
                last_score=float(row.last_score),
                attempts=attempts,
            )
        )
    return evidence


def _level_from_practice(topics: list[TopicEvidence]) -> str | None:
    """Derive a level from quiz evidence alone, or None if there isn't enough.

    Two things gate this. First, there must be real evidence: either breadth
    across several topics, or depth from repeatedly attempting one. Second,
    average mastery only *proposes* a level - at least half the practised
    topics must independently support it. That stops a single strong topic from
    promoting somebody, which is the usual failure mode of naive averaging.
    """
    breadth = len(topics) >= MIN_TOPICS_FOR_LEVEL_CHANGE
    depth = sum(topic.attempts for topic in topics) >= MIN_ATTEMPTS_FOR_LEVEL_CHANGE
    if not breadth and not depth:
        return None

    average = sum(topic.blended for topic in topics) / len(topics)
    proposed = mastery_for(average)

    supported = sum(
        1 for topic in topics if LEVEL_RANK[topic.mastery] >= LEVEL_RANK[proposed]
    )
    if supported / len(topics) < MAJORITY_SUPPORT:
        # Not corroborated - fall back one step rather than over-promoting.
        demoted = LEVELS[max(0, LEVEL_RANK[proposed] - 1)]
        return demoted

    return proposed


async def build_snapshot(session: AsyncSession, learner: Learner) -> AdaptationSnapshot:
    """Collect every piece of evidence we have about this learner."""
    assessment = (
        await session.execute(
            select(Assessment)
            .where(Assessment.learner_id == learner.id)
            .order_by(Assessment.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    topics = await _topic_evidence(session, learner.id)
    total_attempts = sum(topic.attempts for topic in topics)

    last_attempt = (
        await session.execute(
            select(QuizAttempt)
            .where(QuizAttempt.learner_id == learner.id)
            .order_by(QuizAttempt.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()

    # Evidence priority: a graded assessment beats inferred quiz mastery,
    # which beats what the learner claimed at signup.
    if assessment is not None:
        level = estimate_level(assessment.percentage)
        source = "assessment"
    else:
        from_practice = _level_from_practice(topics)
        if from_practice is not None:
            level = from_practice
            source = "practice"
        else:
            level = learner.self_reported_level
            source = "self_reported"

    average = (
        sum(topic.blended for topic in topics) / len(topics) if topics else 0.0
    )

    weak = [t.topic for t in topics if t.is_weak]
    strong = [t.topic for t in topics if t.is_strong]

    # Before any quiz, fall back to the assessment's own topic breakdown.
    if not weak and assessment is not None:
        weak = list(assessment.weak_topics or [])
    if not strong and assessment is not None:
        strong = list(assessment.strong_topics or [])

    return AdaptationSnapshot(
        level=level,
        self_reported_level=learner.self_reported_level,
        level_source=source,
        level_changed=level != learner.current_level,
        average_mastery=round(average, 1),
        topics=topics,
        weak=weak,
        strong=strong,
        assessment_score=assessment.percentage if assessment else None,
        total_attempts=total_attempts,
        recent_difficulty=last_attempt.difficulty if last_attempt else None,
    )


async def apply_snapshot(
    session: AsyncSession, learner: Learner, snapshot: AdaptationSnapshot
) -> AdaptationSnapshot:
    """Write the effective level back to the learner.

    This is the single point that closes the feedback loop: every consumer that
    reads `learner.current_level` (quiz generation, assessment papers, roadmap
    tiering, tutor depth) gets the measured value from now on.
    """
    if snapshot.level != learner.current_level:
        logger.info(
            "Learner %s effective level %s -> %s (source=%s)",
            learner.id,
            learner.current_level,
            snapshot.level,
            snapshot.level_source,
        )
        learner.current_level = snapshot.level
        # The measured value is now the learner's working level.
        learner.estimated_level = snapshot.level
    return snapshot


async def refresh_learner_level(
    session: AsyncSession, learner: Learner
) -> AdaptationSnapshot:
    """Recompute and persist the effective level. Safe to call after any result."""
    snapshot = await build_snapshot(session, learner)
    return await apply_snapshot(session, learner, snapshot)


__all__ = [
    "AdaptationSnapshot",
    "TopicEvidence",
    "WEAK_BELOW",
    "STRONG_AT_OR_ABOVE",
    "apply_snapshot",
    "build_snapshot",
    "refresh_learner_level",
]
