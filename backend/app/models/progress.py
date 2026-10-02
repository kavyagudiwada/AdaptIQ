"""Per-topic progress and mastery model."""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (
        UniqueConstraint("learner_id", "topic", name="uq_progress_learner_topic"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    learner_id: Mapped[int] = mapped_column(
        ForeignKey("learners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    topic: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    progress_percentage: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0
    )
    mastery_level: Mapped[str] = mapped_column(
        Enum("beginner", "intermediate", "advanced", name="mastery_level"),
        nullable=False,
        default="beginner",
    )
    last_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    learner = relationship("Learner", back_populates="progress_records")
