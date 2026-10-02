"""Roadmap request/response schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Difficulty = Literal["easy", "medium", "hard"]


class RoadmapGenerateRequest(BaseModel):
    learner_id: int = Field(gt=0)
    # Without this, a second click is a no-op while the plan is still current,
    # which keeps the endpoint idempotent. With it, the learner can force a
    # rebuild even when the evidence fingerprint is unchanged.
    force: bool = False


class RoadmapTopic(BaseModel):
    name: str
    subtopic: str
    difficulty: Difficulty
    estimated_hours: float
    why_this_matters: str
    resources: list[str]


class RoadmapWeek(BaseModel):
    week: int
    title: str
    focus: str
    topics: list[RoadmapTopic]
    practice_target: int
    milestone: str


class AdaptationOut(BaseModel):
    """How the current plan compares to the learner's latest evidence."""

    is_stale: bool
    revision: int
    effective_level: str
    self_reported_level: str
    level_source: Literal["assessment", "practice", "self_reported"]
    level_changed_from_start: bool
    average_mastery: float
    total_attempts: int
    weak_topics: list[str]
    strong_topics: list[str]
    reasons: list[str] = Field(default_factory=list)
    basis_signature: str | None = None
    current_signature: str | None = None


class RoadmapOut(BaseModel):
    id: int
    learner_id: int
    title: str
    duration: int
    weeks: list[RoadmapWeek]
    personalization_notes: list[str]
    focus_areas: list[str]
    ai_mode: Literal["live", "offline"]
    created_at: datetime
    revision: int = 1
    superseded: bool = False
    completed_weeks: int = 0
    adaptation_reason: str | None = None
    adaptation: AdaptationOut | None = None


class RoadmapCompletionOut(BaseModel):
    """Result of marking another roadmap week as done."""

    completed_weeks: int
    duration: int
    completed: bool
