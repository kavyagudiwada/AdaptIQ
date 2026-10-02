"""Shared FastAPI dependencies."""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Account
from app.services.auth_service import decode_access_token, get_account_by_id

bearer_scheme = HTTPBearer(auto_error=False)


async def current_account(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_db),
) -> Account:
    """Resolve the signed-in account from a `Authorization: Bearer <token>` header."""
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=401, detail="Not authenticated. Please sign in."
        )
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401, detail="Unsupported authorization scheme."
        )

    payload = decode_access_token(credentials.credentials)
    try:
        account_id = int(payload.get("sub", ""))
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=401, detail="Invalid authentication token."
        ) from exc

    return await get_account_by_id(session, account_id)
