"""Adaptive quiz attempt model."""

from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    learner_id: Mapped[int] = mapped_column(
        ForeignKey("learners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    topic: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    difficulty: Mapped[str] = mapped_column(
        Enum(
            "easy",
            "medium",
            "hard",
            name="quiz_difficulty",
        ),
        nullable=False,
        default="medium",
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    # Per-question answer map, e.g. {"q1": 2, "q2": 0}
    answers: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # Confidence calibration: the learner rated every question 1-5 before/while
    # answering. confidence_avg is that average scaled to a 0-100 "how sure I am"
    # percentage; calibration_gap = confidence_avg - accuracy (positive means
    # overconfident).
    confidence_avg: Mapped[float | None] = mapped_column(Float, nullable=True)
    calibration_gap: Mapped[float | None] = mapped_column(Float, nullable=True)
    # {question_id: {"misconception": str, "fix": str}} for every wrong answer.
    misconceptions: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    # Concise calibration coaching from the diagnosis agent.
    calibration_feedback: Mapped[str | None] = mapped_column(
        String(1200), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    learner = relationship("Learner", back_populates="quiz_attempts")

    @property
    def percentage(self) -> float:
        if not self.total_questions:
            return 0.0
        return round(self.score / self.total_questions * 100, 1)
