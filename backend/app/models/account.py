"""Account model: email/password credentials, optionally linked to a learner."""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Account(Base):
    """A person who can sign in.

    Kept separate from `Learner` so adding authentication does not force an
    email/password onto every existing learner row. `learner_id` is filled in
    once the learner completes their profile, which is what makes a returning
    user's personalised dashboard come back with them.
    """

    __tablename__ = "accounts"
    __table_args__ = (
        # Identity is provider-scoped: the same `sub` from two providers is not
        # the same person, and two NULL subjects must not collide.
        UniqueConstraint(
            "auth_provider", "provider_subject", name="uq_accounts_provider_subject"
        ),
        # Password sign-in is only ever offered to 'password' accounts.
        Index(
            "ix_accounts_email_password_provider", "email", "auth_provider"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(320), nullable=False, unique=True, index=True
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # NULL for accounts that authenticate through an external provider.
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    # 'password' or 'google'. Password sign-in is only offered to 'password'.
    auth_provider: Mapped[str] = mapped_column(
        String(16), nullable=False, default="password"
    )
    # The provider's stable user identifier (Google's `sub`).
    provider_subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    learner_id: Mapped[int | None] = mapped_column(
        ForeignKey("learners.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    learner = relationship("Learner", lazy="selectin")
