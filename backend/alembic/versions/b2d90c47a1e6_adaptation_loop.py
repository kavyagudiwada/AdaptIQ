"""adaptation loop: self-reported level + roadmap revision tracking

Revision ID: b2d90c47a1e6
Revises: c4f8a1d92e37
Create Date: 2026-09-27 01:20:44.771902
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "b2d90c47a1e6"
down_revision: Union[str, None] = "c4f8a1d92e37"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# The enum types already exist from the initial schema, so only reuse them.
LEARNER_LEVEL = postgresql.ENUM(
    "beginner", "intermediate", "advanced", name="learner_level", create_type=False
)


def upgrade() -> None:
    # 1. Keep what the learner originally claimed, so we can show them the gap
    #    between "you said beginner" and "we measured intermediate".
    op.add_column(
        "learners",
        sa.Column("self_reported_level", LEARNER_LEVEL, nullable=True),
    )
    op.execute("UPDATE learners SET self_reported_level = current_level")
    op.alter_column(
        "learners",
        "self_reported_level",
        existing_type=LEARNER_LEVEL,
        nullable=False,
        server_default="beginner",
    )

    # 2. Track how many times a plan has been rebuilt, what evidence it was
    #    built from, and which revision is current.
    op.add_column(
        "roadmaps",
        sa.Column("revision", sa.Integer(), nullable=False, server_default="1"),
    )
    op.add_column(
        "roadmaps",
        sa.Column("basis_signature", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "roadmaps",
        sa.Column(
            "superseded", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )
    op.add_column(
        "roadmaps",
        sa.Column("adaptation_reason", sa.String(length=255), nullable=True),
    )

    # get_roadmap() reads the newest non-superseded plan.
    op.create_index(
        "ix_roadmaps_learner_id_superseded",
        "roadmaps",
        ["learner_id", "superseded"],
    )


def downgrade() -> None:
    op.drop_index("ix_roadmaps_learner_id_superseded", table_name="roadmaps")
    op.drop_column("roadmaps", "adaptation_reason")
    op.drop_column("roadmaps", "superseded")
    op.drop_column("roadmaps", "basis_signature")
    op.drop_column("roadmaps", "revision")
    op.drop_column("learners", "self_reported_level")
