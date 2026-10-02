"""Progress and health schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.schemas.learner import Level
from app.schemas.quiz import Difficulty


class TopicProgressOut(BaseModel):
    topic: str
    progress_percentage: float
    mastery_level: Level
    last_score: float
    updated_at: datetime


class QuizHistoryPoint(BaseModel):
    attempt_id: int
    topic: str
    difficulty: Difficulty
    percentage: float
    confidence_avg: float | None = None
    calibration_gap: float | None = None
    created_at: datetime


class ActivityItem(BaseModel):
    label: str
    detail: str
    kind: Literal["profile", "assessment", "roadmap", "tutor", "quiz"]
    created_at: datetime


class ProgressOut(BaseModel):
    learner_id: int
    learner_name: str
    topic: str
    overall_progress: float
    assessment_percentage: float | None = None
    estimated_level: Level
    current_topic: str
    recommended_next_topic: str
    recommendation_reason: str
    topics: list[TopicProgressOut]
    strong_topics: list[str]
    weak_topics: list[str]
    quiz_history: list[QuizHistoryPoint]
    # Absolute calibration gap averaged over attempts that recorded a
    # confidence rating. Lower is better: 0 means the learner's confidence
    # matched their accuracy, positive means overconfident on average.
    calibration_avg_gap: float | None = None
    learning_streak: int
    total_quizzes: int
    total_tutor_sessions: int
    roadmap_weeks_completed: int
    recent_activity: list[ActivityItem]
    ai_mode: Literal["live", "offline"]


class HealthOut(BaseModel):
    status: str
    database: str
    ai_provider: str
    ai_mode: Literal["live", "offline"]
    version: str
