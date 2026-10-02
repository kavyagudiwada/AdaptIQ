"""Personalised learning roadmap model."""

from datetime import datetime

from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"
    # Supports the hot query: "the active plan for this learner".
    __table_args__ = (
        Index("ix_roadmaps_learner_id_superseded", "learner_id", "superseded"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    learner_id: Mapped[int] = mapped_column(
        ForeignKey("learners.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    # How many weeks the learner has marked as done. Drives the dashboard's
    # "X of Y weeks completed" figure and lets the plan feel checkable.
    completed_weeks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Full week-by-week structure produced by the roadmap agent.
    roadmap_data: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    focus_areas: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list
    )
    # How many times this learner's plan has been rebuilt (1 = first plan).
    revision: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    # Fingerprint of the evidence the plan was built from. When the learner's
    # evidence no longer matches this, the plan is considered stale and the
    # tutor can offer to adapt it.
    basis_signature: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Older plans are kept for history rather than orphaned by an INSERT.
    superseded: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Human-readable "why this plan changed", shown to the learner.
    adaptation_reason: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    learner = relationship("Learner", back_populates="roadmaps")
