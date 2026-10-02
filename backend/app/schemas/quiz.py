"""Quiz request/response schemas."""

from typing import Literal

from pydantic import BaseModel, Field

Difficulty = Literal["easy", "medium", "hard"]


class QuizGenerateRequest(BaseModel):
    learner_id: int = Field(gt=0)
    topic: str | None = Field(default=None, max_length=120)


class QuizQuestionOut(BaseModel):
    id: str
    question: str
    options: list[str]
    correct_index: int
    subtopic: str
    difficulty: Difficulty
    explanation: str


class QuizOut(BaseModel):
    quiz_id: int | None = None
    learner_id: int
    topic: str
    difficulty: Difficulty
    questions: list[QuizQuestionOut]
    total_questions: int
    adaptation_note: str
    previous_percentage: float | None = None
    ai_mode: Literal["live", "offline"]


class QuizAnswer(BaseModel):
    question_id: str
    selected_index: int = Field(ge=0, le=3)
    # Learner's self-assessed confidence 1 (guessing) to 5 (very sure).
    confidence: int | None = Field(default=None, ge=1, le=5)


class QuizSubmitRequest(BaseModel):
    learner_id: int = Field(gt=0)
    topic: str = Field(min_length=1, max_length=120)
    difficulty: Difficulty
    answers: list[QuizAnswer] = Field(min_length=1)
    # The exact paper the learner answered. When present we grade against it
    # (and diagnose misconceptions on the text they actually saw) instead of
    # regenerating. Optional so older clients keep working.
    paper: list[QuizQuestionOut] | None = None
    # Mode the paper was generated in, echoed back into the result.
    ai_mode: Literal["live", "offline"] | None = None


class MisconceptionOut(BaseModel):
    question_id: str
    misconception: str
    fix: str


class QuizReviewItem(BaseModel):
    question_id: str
    question: str
    subtopic: str
    your_answer: str
    correct_answer: str
    was_correct: bool
    explanation: str
    misconception: str | None = None
    misconception_fix: str | None = None


class QuizResultOut(BaseModel):
    attempt_id: int
    learner_id: int
    topic: str
    difficulty: Difficulty
    score: int
    total_questions: int
    percentage: float
    next_difficulty: Difficulty
    difficulty_changed: bool
    system_message: str
    weak_topics: list[str]
    strong_topics: list[str]
    recommended_action: str
    ai_mode: Literal["live", "offline"]
    # The learner's effective level after this attempt, so the tutor can tell
    # them when practice has moved them up or down a band.
    current_level: str | None = None
    level_changed: bool = False
    level_source: Literal["assessment", "practice", "self_reported"] | None = None
    roadmap_stale: bool = False
    # Question-by-question review with misconception diagnosis for wrong answers.
    review: list[QuizReviewItem] = []
    misconceptions: list[MisconceptionOut] = []
    # Confidence calibration (None when the learner skipped the ratings).
    confidence_avg: float | None = None
    calibration_gap: float | None = None
    calibration_feedback: str | None = None
