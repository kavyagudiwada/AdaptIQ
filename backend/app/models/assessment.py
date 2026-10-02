"""Initial assessment model: score plus strong / weak topic analysis."""

from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    learner_id: Mapped[int] = mapped_column(
        ForeignKey("learners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    strong_topics: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    weak_topics: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    learner = relationship("Learner", back_populates="assessments")

    @property
    def percentage(self) -> float:
        if not self.total_questions:
            return 0.0
        return round(self.score / self.total_questions * 100, 1)

    @property
    def estimated_level(self) -> str:
        pct = self.percentage
        if pct >= 75:
            return "advanced"
        if pct >= 45:
            return "intermediate"
        return "beginner"
