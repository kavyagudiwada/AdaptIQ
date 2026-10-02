"""Tutor request/response schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Difficulty = Literal["easy", "medium", "hard"]


class TutorExplainRequest(BaseModel):
    learner_id: int = Field(gt=0)
    topic: str = Field(min_length=1, max_length=120)
    question: str | None = Field(default=None, max_length=1000)
    difficulty: Difficulty | None = None


class TutorResponseOut(BaseModel):
    topic: str
    explanation: str
    example: str
    key_points: list[str]
    common_mistakes: list[str]
    follow_up_question: str
    difficulty: Difficulty
    personalized_note: str
    ai_mode: Literal["live", "offline"]


class TutorHistoryItem(BaseModel):
    """A saved tutor explanation the learner can revisit."""

    id: int
    topic: str
    subtopic: str
    difficulty: Difficulty
    explanation: str
    example: str
    key_points: list[str]
    common_mistakes: list[str]
    ai_mode: Literal["live", "offline"]
    created_at: datetime


class TutorHistoryOut(BaseModel):
    sessions: list[TutorHistoryItem]
