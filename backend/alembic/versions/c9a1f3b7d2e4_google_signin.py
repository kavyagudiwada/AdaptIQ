"""google sign-in: nullable password + provider identity columns

Revision ID: c9a1f3b7d2e4
Revises: b2d90c47a1e6
Create Date: 2026-09-27 04:05:12.339041
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c9a1f3b7d2e4"
down_revision: Union[str, None] = "b2d90c47a1e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # A Google account never has a password, so the column has to allow NULL.
    op.alter_column(
        "accounts",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=True,
    )
    op.add_column(
        "accounts",
        sa.Column(
            "auth_provider",
            sa.String(length=16),
            nullable=False,
            server_default="password",
        ),
    )
    op.add_column(
        "accounts",
        sa.Column("provider_subject", sa.String(length=255), nullable=True),
    )
    # Identity is provider-scoped: the same `sub` from two providers is not
    # the same person, and two NULL subjects must not collide with each other.
    op.create_unique_constraint(
        "uq_accounts_provider_subject",
        "accounts",
        ["auth_provider", "provider_subject"],
    )
    # Password sign-in should only ever consider password accounts.
    op.create_index(
        "ix_accounts_email_password_provider",
        "accounts",
        ["email", "auth_provider"],
    )


def downgrade() -> None:
    op.drop_index("ix_accounts_email_password_provider", table_name="accounts")
    op.drop_constraint("uq_accounts_provider_subject", "accounts", type_="unique")

    # Any Google-only account cannot be represented once the column is NOT NULL.
    op.execute("DELETE FROM accounts WHERE password_hash IS NULL")
    op.alter_column(
        "accounts",
        "password_hash",
        existing_type=sa.String(length=255),
        nullable=False,
    )
    op.drop_column("accounts", "provider_subject")
    op.drop_column("accounts", "auth_provider")
