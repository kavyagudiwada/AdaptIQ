"""accounts table

Revision ID: c4f8a1d92e37
Revises: e7790b02be17
Create Date: 2026-09-26 23:58:11.204417
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c4f8a1d92e37"
down_revision: Union[str, None] = "e7790b02be17"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("learner_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["learner_id"], ["learners.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_accounts_email", "accounts", ["email"], unique=True)
    op.create_index("ix_accounts_learner_id", "accounts", ["learner_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_accounts_learner_id", table_name="accounts")
    op.drop_index("ix_accounts_email", table_name="accounts")
    op.drop_table("accounts")
