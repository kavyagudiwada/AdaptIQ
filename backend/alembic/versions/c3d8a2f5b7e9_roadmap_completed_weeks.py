"""learner-marked roadmap completion weeks

Revision ID: c3d8a2f5b7e9
Revises: a7f3c9b51d20
Create Date: 2026-10-02 10:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c3d8a2f5b7e9"
down_revision: Union[str, None] = "a7f3c9b51d20"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "roadmaps",
        sa.Column("completed_weeks", sa.Integer(), server_default="0", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("roadmaps", "completed_weeks")