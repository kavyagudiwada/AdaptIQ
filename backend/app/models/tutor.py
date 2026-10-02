"""Persisted AI tutor session model.

Every explanation is stored so the progress page can count real tutor sessions
and the learner can revisit what they were taught.
"""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON, Text

from app.core.database import Base


class TutorSession(Base):
    __tablename__ = "tutor_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    learner_id: Mapped[int] = mapped_column(
        ForeignKey("learners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    topic: Mapped[str] = mapped_column(String(120), nullable=False)
    subtopic: Mapped[str] = mapped_column(String(120), nullable=False)
    question: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    difficulty: Mapped[str] = mapped_column(
        Enum("easy", "medium", "hard", name="quiz_difficulty"),
        nullable=False,
        default="medium",
    )
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    example: Mapped[str] = mapped_column(Text, nullable=False, default="")
    key_points: Mapped[list | None] = mapped_column(JSON, nullable=True)
    common_mistakes: Mapped[list | None] = mapped_column(JSON, nullable=True)
    follow_up_question: Mapped[str | None] = mapped_column(Text, nullable=True)
    personalized_note: Mapped[str | None] = mapped_column(
        String(1200), nullable=True
    )
    ai_mode: Mapped[str] = mapped_column(
        String(16), nullable=False, default="offline"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    learner = relationship("Learner", back_populates="tutor_sessions")