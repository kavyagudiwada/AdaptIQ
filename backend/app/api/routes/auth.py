"""Authentication endpoints."""

import logging
from typing import Annotated
from urllib.parse import quote

from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import RedirectResponse

from app.api.deps import current_account
from app.core.config import settings
from app.core.database import DbSession
from app.models import Account
from app.schemas.auth import (
    AccountOut,
    AuthTokenOut,
    GoogleExchangeRequest,
    GoogleStatusOut,
    LinkLearnerRequest,
    LoginRequest,
    RegisterRequest,
)
from app.services import google_auth_service
from app.services.auth_service import (
    authenticate,
    link_learner,
    register_account,
)

router = APIRouter(prefix="/auth", tags=["auth"])

logger = logging.getLogger(__name__)

CurrentAccount = Annotated[Account, Depends(current_account)]


@router.post(
    "/register", response_model=AuthTokenOut, status_code=status.HTTP_201_CREATED
)
async def register(
    payload: RegisterRequest, session: DbSession
) -> AuthTokenOut:
    """Create an account and return a ready-to-use bearer token."""
    return await register_account(session, payload)


@router.post("/login", response_model=AuthTokenOut)
async def login(payload: LoginRequest, session: DbSession) -> AuthTokenOut:
    """Exchange email + password for a bearer token."""
    return await authenticate(session, payload)


@router.get("/me", response_model=AccountOut)
async def read_me(account: CurrentAccount) -> AccountOut:
    """Return the account behind the supplied bearer token."""
    return AccountOut.model_validate(account)


@router.post("/me/learner", response_model=AccountOut)
async def attach_learner(
    payload: LinkLearnerRequest, account: CurrentAccount, session: DbSession
) -> AccountOut:
    """Link a learner record to this account so progress is restored on sign-in."""
    linked = await link_learner(session, account, payload)
    return AccountOut.model_validate(linked)


@router.get("/google/status", response_model=GoogleStatusOut)
async def google_status() -> GoogleStatusOut:
    """Whether Google sign-in is configured, so the UI can adapt."""
    return GoogleStatusOut(enabled=settings.google_enabled)


@router.get("/google/start")
async def google_start(request: Request) -> RedirectResponse:
    """Begin the OAuth flow by redirecting to Google's consent screen."""
    google_auth_service.require_google_enabled()
    state = google_auth_service.new_state()
    return RedirectResponse(
        google_auth_service.authorization_url(state, request),
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


@router.get("/google/callback", name="google_callback")
async def google_callback(
    request: Request,
    session: DbSession,
    code: str | None = Query(default=None),
    state: str | None = Query(default=None),
    error: str | None = Query(default=None),
) -> RedirectResponse:
    """Handle Google's redirect and hand the frontend a single-use code.

    On any failure the user is returned to the login page with a `reason` the
    frontend can explain, rather than being shown a raw provider error.
    """
    frontend = settings.frontend_url.rstrip("/")

    def back_to_login(reason: str | None = None) -> RedirectResponse:
        target = f"{frontend}/auth/google/callback"
        if reason:
            target = f"{target}?error={quote(reason)}"
        return RedirectResponse(target, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    if error:
        logger.warning("Google sign-in declined: %s", error)
        return back_to_login("Google sign-in was cancelled.")
    if not google_auth_service.consume_state(state):
        logger.warning("Google callback rejected: bad or missing state")
        return back_to_login("That sign-in attempt expired. Please try again.")
    if not code:
        return back_to_login("Google did not return a sign-in code.")

    try:
        account = await google_auth_service.resolve_google_identity(
            session, code, request
        )
    except HTTPException as exc:
        logger.warning("Google sign-in failed: %s", exc.detail)
        return back_to_login(str(exc.detail))

    return RedirectResponse(
        f"{frontend}/auth/google/callback?code={quote(google_auth_service.issue_exchange_code(account))}",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


@router.post("/google/exchange", response_model=AuthTokenOut)
async def google_exchange(
    payload: GoogleExchangeRequest, session: DbSession
) -> AuthTokenOut:
    """Swap the single-use code for a bearer token. The code cannot be reused."""
    return await google_auth_service.redeem_exchange_code(session, payload.code)
