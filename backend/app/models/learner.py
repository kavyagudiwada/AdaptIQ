"""Learner profile model."""

from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Learner(Base):
    __tablename__ = "learners"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    topic: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    current_level: Mapped[str] = mapped_column(
        Enum("beginner", "intermediate", "advanced", name="learner_level"),
        nullable=False,
        default="beginner",
    )
    # What the learner claimed at signup, kept verbatim. `current_level` is the
    # *effective* level and is rewritten from real evidence, so without this
    # column the original claim would be lost the first time they level up.
    self_reported_level: Mapped[str] = mapped_column(
        Enum("beginner", "intermediate", "advanced", name="learner_level"),
        nullable=False,
        default="beginner",
    )
    learning_goal: Mapped[str] = mapped_column(
        Enum(
            "academic",
            "placement",
            "interview",
            "project",
            "general",
            name="learning_goal",
        ),
        nullable=False,
        default="general",
    )
    hours_per_week: Mapped[float] = mapped_column(Float, nullable=False, default=5)
    target_duration: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    estimated_level: Mapped[str | None] = mapped_column(
        Enum("beginner", "intermediate", "advanced", name="estimated_level"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    assessments = relationship(
        "Assessment",
        back_populates="learner",
        cascade="all, delete-orphan",
    )
    roadmaps = relationship(
        "Roadmap",
        back_populates="learner",
        cascade="all, delete-orphan",
    )
    quiz_attempts = relationship(
        "QuizAttempt",
        back_populates="learner",
        cascade="all, delete-orphan",
    )
    progress_records = relationship(
        "Progress",
        back_populates="learner",
        cascade="all, delete-orphan",
    )
    tutor_sessions = relationship(
        "TutorSession",
        back_populates="learner",
        cascade="all, delete-orphan",
    )
