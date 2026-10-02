"""Authentication: password hashing, credential checks and token issuing."""

from __future__ import annotations

import base64
import hashlib
import logging
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models import Account, Learner
from app.schemas.auth import (
    AccountOut,
    AuthTokenOut,
    LinkLearnerRequest,
    LoginRequest,
    RegisterRequest,
)

logger = logging.getLogger(__name__)

INVALID_CREDENTIALS = "That email and password combination is incorrect."

# bcrypt silently ignores anything past 72 bytes, so every password is reduced
# to a fixed-width digest first. That keeps long passphrases fully significant.
_BCRYPT_ROUNDS = 12
_ephemeral_secret: str | None = None


def _prepare(password: str) -> bytes:
    """Reduce any password to a fixed 44-byte, bcrypt-safe value."""
    return base64.b64encode(hashlib.sha256(password.encode("utf-8")).digest())


def signing_key() -> str:
    """Return the configured secret, or an ephemeral one for local development."""
    global _ephemeral_secret

    configured = settings.jwt_secret.strip()
    if configured:
        return configured
    if _ephemeral_secret is None:
        _ephemeral_secret = secrets.token_urlsafe(48)
        logger.warning(
            "JWT_SECRET is not set - generated an ephemeral signing key. "
            "Sessions will not survive a restart. Set JWT_SECRET for real use."
        )
    return _ephemeral_secret


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        _prepare(password), bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    ).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(_prepare(password), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        # Malformed hash in the database: treat as a failed login, never crash.
        logger.warning("Stored password hash is not valid bcrypt")
        return False


def create_access_token(account: Account) -> tuple[str, int]:
    """Return a signed JWT and its lifetime in seconds."""
    now = datetime.now(timezone.utc)
    expires_in = settings.jwt_expiry_minutes * 60
    payload = {
        "sub": str(account.id),
        "email": account.email,
        "name": account.name,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_expiry_minutes)).timestamp()),
    }
    token = jwt.encode(payload, signing_key(), algorithm=settings.jwt_algorithm)
    return token, expires_in


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, signing_key(), algorithms=[settings.jwt_algorithm]
        )
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=401, detail="Your session has expired. Please sign in again."
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=401, detail="Invalid authentication token."
        ) from exc


async def get_account_by_email(session: AsyncSession, email: str) -> Account | None:
    return await session.scalar(select(Account).where(Account.email == email))


async def get_account_by_id(session: AsyncSession, account_id: int) -> Account:
    account = await session.get(Account, account_id)
    if account is None:
        raise HTTPException(status_code=401, detail="Account no longer exists.")
    return account


def _token_response(account: Account, token: str, expires_in: int) -> AuthTokenOut:
    return AuthTokenOut(
        access_token=token,
        expires_in=expires_in,
        account=AccountOut.model_validate(account),
        learner_id=account.learner_id,
    )


async def register_account(
    session: AsyncSession, payload: RegisterRequest
) -> AuthTokenOut:
    """Create an account and sign the new user straight in."""
    if await get_account_by_email(session, payload.email) is not None:
        raise HTTPException(
            status_code=409, detail="An account with that email already exists."
        )

    account = Account(
        email=payload.email,
        name=payload.name,
        password_hash=hash_password(payload.password),
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)

    token, expires_in = create_access_token(account)
    logger.info("Account %s registered (id=%s)", account.email, account.id)
    return _token_response(account, token, expires_in)


async def authenticate(
    session: AsyncSession, payload: LoginRequest
) -> AuthTokenOut:
    """Verify credentials and issue a token.

    An unknown email, a wrong password and an account that has no password at
    all (Google-only) all return the identical 401, so the endpoint cannot be
    used to discover which addresses have accounts or how they sign in.
    """
    account = await get_account_by_email(session, payload.email)
    if account is None or not account.password_hash:
        raise HTTPException(status_code=401, detail=INVALID_CREDENTIALS)
    if not verify_password(payload.password, account.password_hash):
        raise HTTPException(status_code=401, detail=INVALID_CREDENTIALS)

    token, expires_in = create_access_token(account)
    logger.info("Account %s signed in (id=%s)", account.email, account.id)
    return _token_response(account, token, expires_in)


async def link_learner(
    session: AsyncSession, account: Account, payload: LinkLearnerRequest
) -> Account:
    """Attach a learner record so future sign-ins restore that progress."""
    learner = await session.get(Learner, payload.learner_id)
    if learner is None:
        raise HTTPException(
            status_code=404, detail=f"Learner {payload.learner_id} not found."
        )

    account.learner_id = learner.id
    await session.commit()
    await session.refresh(account)
    return account
