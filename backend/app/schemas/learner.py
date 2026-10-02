"""Learner request/response schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Level = Literal["beginner", "intermediate", "advanced"]
LearningGoal = Literal["academic", "placement", "interview", "project", "general"]


class LearnerProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120, examples=["Kavya"])
    topic: str = Field(min_length=1, max_length=120, examples=["Machine Learning"])
    current_level: Level = "beginner"
    learning_goal: LearningGoal = "general"
    hours_per_week: float = Field(gt=0, le=80, examples=[5])
    target_duration: int = Field(gt=0, le=52, examples=[4])


class LearnerProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    topic: str
    # The effective level, rewritten from real evidence.
    current_level: Level
    # What the learner claimed at signup, kept so we can show the gap.
    self_reported_level: Level = "beginner"
    learning_goal: LearningGoal
    hours_per_week: float
    target_duration: int
    estimated_level: Level | None = None
    created_at: datetime
