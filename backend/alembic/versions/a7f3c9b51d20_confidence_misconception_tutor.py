"""confidence calibration + misconception diagnosis + persisted tutor sessions

Revision ID: a7f3c9b51d20
Revises: b2d90c47a1e6
Create Date: 2026-09-29 09:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "a7f3c9b51d20"
down_revision: Union[str, None] = "c9a1f3b7d2e4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# The enum type already exists from the initial schema, so only reuse it.
QUIZ_DIFFICULTY = postgresql.ENUM(
    "easy", "medium", "hard", name="quiz_difficulty", create_type=False
)


def upgrade() -> None:
    # 1. Calibration + misconception diagnosis stored on each quiz attempt.
    op.add_column(
        "quiz_attempts",
        sa.Column("confidence_avg", sa.Float(), nullable=True),
    )
    op.add_column(
        "quiz_attempts",
        sa.Column("calibration_gap", sa.Float(), nullable=True),
    )
    op.add_column(
        "quiz_attempts",
        sa.Column(
            "misconceptions",
            sa.JSON(),
            nullable=True,
        ),
    )
    op.add_column(
        "quiz_attempts",
        sa.Column("calibration_feedback", sa.String(length=1200), nullable=True),
    )

    # 2. Persisted AI tutor sessions.
    op.create_table(
        "tutor_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("learner_id", sa.Integer(), nullable=False),
        sa.Column("topic", sa.String(length=120), nullable=False),
        sa.Column("subtopic", sa.String(length=120), nullable=False),
        sa.Column("question", sa.String(length=1000), nullable=True),
        sa.Column("difficulty", QUIZ_DIFFICULTY, nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("example", sa.Text(), nullable=False),
        sa.Column("key_points", sa.JSON(), nullable=True),
        sa.Column("common_mistakes", sa.JSON(), nullable=True),
        sa.Column("follow_up_question", sa.Text(), nullable=True),
        sa.Column("personalized_note", sa.String(length=1200), nullable=True),
        sa.Column("ai_mode", sa.String(length=16), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["learner_id"], ["learners.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_tutor_sessions_learner_id"),
        "tutor_sessions",
        ["learner_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_tutor_sessions_learner_id"), table_name="tutor_sessions")
    op.drop_table("tutor_sessions")
    op.drop_column("quiz_attempts", "calibration_feedback")
    op.drop_column("quiz_attempts", "misconceptions")
    op.drop_column("quiz_attempts", "calibration_gap")
    op.drop_column("quiz_attempts", "confidence_avg")