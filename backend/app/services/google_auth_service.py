"""Google sign-in (OIDC authorization-code flow).

Design notes:

* The browser never sees a bearer token in a URL. Google redirects back to
  `/auth/google/callback`, we verify the CSRF `state`, resolve the account, and
  then hand the frontend a short-lived **one-time code**. The frontend POSTs
  that code to `/auth/google/exchange` to collect the real token. Tokens in
  query strings leak into history, referrers and access logs, so we avoid them.
* The `state` and the one-time code are both short-lived **signed JWTs**, not
  process-local map entries, so the flow survives container recycles and any
  number of workers without a shared cache (see `new_state` / `issue_exchange_code`).
* Google-only accounts have no password, so `Account.password_hash` is NULL and
  password sign-in must not be offered for them (see `auth_service.authenticate`).
"""

from __future__ import annotations

import logging
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import httpx
import jwt
from fastapi import HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models import Account
from app.schemas.auth import AuthTokenOut
from app.services.auth_service import (_token_response, create_access_token,
                                       signing_key)

logger = logging.getLogger(__name__)

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

SCOPES = "openid email profile"

HTTP_TIMEOUT = 20.0

# How long an in-flight OAuth `state` stays valid, and how long a handed-off
# one-time code may be exchanged for a token.
STATE_TTL_SECONDS = 600
EXCHANGE_CODE_TTL_SECONDS = 120


def require_google_enabled() -> None:
    if not settings.google_enabled:
        raise HTTPException(
            status_code=503,
            detail="Google sign-in is not configured on this server.",
        )


def callback_url(request: Request) -> str:
    """Absolute Google redirect URI, derived from the incoming request.

    Deriving it means the same code works on localhost, on a LAN IP and behind
    a reverse proxy without a second setting to keep in sync. It must match the
    redirect URI registered in the Google Cloud console exactly.
    """
    return f"{str(request.base_url).rstrip('/')}/api/auth/google/callback"


def new_state() -> str:
    """Mint the CSRF `state` carried through the Google round trip.

    A short-lived signed JWT instead of an entry in a process-local map, so the
    value survives container recycles and can be verified by any worker. The
    signature binds it to this installation and this signing key; expiry keeps
    stale flows from being redeemed.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "purpose": "google-oauth-state",
        "nonce": secrets.token_urlsafe(12),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=STATE_TTL_SECONDS)).timestamp()),
    }
    return jwt.encode(payload, signing_key(), algorithm=settings.jwt_algorithm)


def consume_state(state: str | None) -> bool:
    """Reject a callback whose state we did not issue (CSRF protection)."""
    if not state:
        return False
    try:
        payload = jwt.decode(
            state, signing_key(), algorithms=[settings.jwt_algorithm]
        )
    except jwt.InvalidTokenError:
        return False
    return payload.get("purpose") == "google-oauth-state"


def authorization_url(state: str, request: Request) -> str:
    params = {
        "client_id": settings.google_client_id.strip(),
        "redirect_uri": callback_url(request),
        "response_type": "code",
        "scope": SCOPES,
        "state": state,
        "access_type": "offline",
        "prompt": "select_account",
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


async def _exchange_code(code: str, request: Request) -> dict:
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.google_client_id.strip(),
                    "client_secret": settings.google_client_secret.strip(),
                    "redirect_uri": callback_url(request),
                    "grant_type": "authorization_code",
                },
            )
    except httpx.HTTPError as exc:
        logger.warning("Google token exchange transport error: %s", exc)
        raise HTTPException(
            status_code=502, detail="Could not reach Google. Please try again."
        ) from exc

    if response.status_code != 200:
        logger.warning("Google token exchange failed: %s %s", response.status_code, response.text)
        raise HTTPException(
            status_code=502, detail="Google rejected the sign-in attempt."
        )
    return response.json()


async def _fetch_userinfo(access_token: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
            response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
    except httpx.HTTPError as exc:
        logger.warning("Google userinfo transport error: %s", exc)
        raise HTTPException(
            status_code=502, detail="Could not reach Google. Please try again."
        ) from exc

    if response.status_code != 200:
        raise HTTPException(
            status_code=502, detail="Could not read your Google profile."
        )
    return response.json()


async def get_or_create_google_account(
    session: AsyncSession, subject: str, email: str, name: str
) -> Account:
    """Resolve a Google identity to a local account, creating one if needed.

    Two cases are merged deliberately: the same Google user signing in twice
    always finds their account, and a person who previously registered with a
    password using the same email adopts that existing account rather than
    ending up with two profiles.
    """
    result = await session.execute(
        select(Account).where(
            Account.auth_provider == "google",
            Account.provider_subject == subject,
        )
    )
    account = result.scalar_one_or_none()
    if account is not None:
        # Google can change a display name; keep ours current.
        if name and account.name != name:
            account.name = name
            await session.commit()
            await session.refresh(account)
        return account

    by_email = await session.execute(
        select(Account).where(Account.email == email)
    )
    existing = by_email.scalar_one_or_none()
    if existing is not None:
        existing.auth_provider = "google"
        existing.provider_subject = subject
        if not existing.password_hash:
            existing.name = name or existing.name
        await session.commit()
        await session.refresh(existing)
        logger.info("Account %s linked to Google (id=%s)", existing.email, existing.id)
        return existing

    account = Account(
        email=email,
        name=name or email.split("@", 1)[0],
        password_hash=None,
        auth_provider="google",
        provider_subject=subject,
    )
    session.add(account)
    await session.commit()
    await session.refresh(account)
    logger.info("Account %s created via Google (id=%s)", account.email, account.id)
    return account


async def resolve_google_identity(
    session: AsyncSession, code: str, request: Request
) -> Account:
    """Turn an authorization code into a local account."""
    tokens = await _exchange_code(code, request)
    access_token = tokens.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=502, detail="Google did not return an access token."
        )

    profile = await _fetch_userinfo(access_token)
    subject = profile.get("sub")
    email = (profile.get("email") or "").strip().lower()
    if not subject or not email:
        raise HTTPException(
            status_code=502, detail="Your Google account did not share an email address."
        )
    if profile.get("email_verified") is False:
        raise HTTPException(
            status_code=400, detail="Your Google email address is not verified."
        )

    return await get_or_create_google_account(
        session, subject=subject, email=email, name=(profile.get("name") or "").strip()
    )


def issue_exchange_code(account: Account) -> str:
    """Mint the one-time code the frontend swaps for a bearer token.

    The code is a short-lived signed JWT, not an entry in a process-local map,
    so it survives container recycles (Render free instances restart at any
    time). Its brevity and signature prevent reuse and forgery; the account id
    is carried inside, so redemption needs no shared store.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(account.id),
        "purpose": "google-signin-exchange",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=EXCHANGE_CODE_TTL_SECONDS)).timestamp()),
    }
    return jwt.encode(payload, signing_key(), algorithm=settings.jwt_algorithm)


async def redeem_exchange_code(session: AsyncSession, code: str) -> AuthTokenOut:
    try:
        payload = jwt.decode(
            code, signing_key(), algorithms=[settings.jwt_algorithm]
        )
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=400,
            detail="That sign-in link has expired. Please try again.",
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=400,
            detail="That sign-in link has expired. Please try again.",
        ) from exc
    if payload.get("purpose") != "google-signin-exchange":
        raise HTTPException(
            status_code=400,
            detail="That sign-in link has expired. Please try again.",
        )
    account_id = payload.get("sub")
    if not account_id:
        raise HTTPException(
            status_code=400,
            detail="That sign-in link has expired. Please try again.",
        )
    account = await session.get(Account, int(account_id))
    if account is None:
        raise HTTPException(status_code=401, detail="Account no longer exists.")
    token, expires_in = create_access_token(account)
    return _token_response(account, token, expires_in)


__all__ = [
    "authorization_url",
    "callback_url",
    "consume_state",
    "issue_exchange_code",
    "new_state",
    "redeem_exchange_code",
    "require_google_enabled",
    "resolve_google_identity",
]
