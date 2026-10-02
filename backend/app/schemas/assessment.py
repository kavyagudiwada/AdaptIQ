"""Assessment request/response schemas."""

from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.learner import Level

Difficulty = Literal["easy", "medium", "hard"]


class AssessmentGenerateRequest(BaseModel):
    learner_id: int = Field(gt=0)


class AssessmentQuestionOut(BaseModel):
    id: str
    question: str
    options: list[str]
    correct_index: int
    subtopic: str
    difficulty: Difficulty


class AssessmentPaperOut(BaseModel):
    assessment_id: int | None = None
    learner_id: int
    questions: list[AssessmentQuestionOut]
    total_questions: int
    ai_mode: Literal["live", "offline"]


class AssessmentAnswer(BaseModel):
    question_id: str
    selected_index: int = Field(ge=0, le=3)


class AssessmentSubmitRequest(BaseModel):
    learner_id: int = Field(gt=0)
    answers: list[AssessmentAnswer] = Field(min_length=1)


class TopicBreakdown(BaseModel):
    subtopic: str
    correct: int
    total: int
    percentage: float


class AssessmentResultOut(BaseModel):
    assessment_id: int
    learner_id: int
    score: int
    total_questions: int
    percentage: float
    strong_topics: list[str]
    weak_topics: list[str]
    estimated_level: Level
    topic_breakdown: list[TopicBreakdown]
    feedback: str
    ai_mode: Literal["live", "offline"]
