"""Authentication request/response schemas."""

import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Deliberately simple: one @, no spaces, a dotted domain with a 2+ char TLD.
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")


def _normalise_email(value: str) -> str:
    email = value.strip().lower()
    if not EMAIL_PATTERN.match(email):
        raise ValueError("Enter a valid email address.")
    return email


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120, examples=["Kavya"])
    email: str = Field(min_length=5, max_length=320, examples=["kavya@example.com"])
    password: str = Field(min_length=8, max_length=128, examples=["correct-horse-battery"])

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return _normalise_email(value)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        name = value.strip()
        if not name:
            raise ValueError("Please enter your name.")
        return name


class LoginRequest(BaseModel):
    email: str = Field(min_length=1, max_length=320, examples=["kavya@example.com"])
    password: str = Field(min_length=1, max_length=128, examples=["correct-horse-battery"])

    @field_validator("email")
    @classmethod
    def normalise_email(cls, value: str) -> str:
        return value.strip().lower()


class LinkLearnerRequest(BaseModel):
    learner_id: int = Field(gt=0, examples=[12])


class GoogleExchangeRequest(BaseModel):
    """Single-use code minted by the Google callback."""

    code: str = Field(min_length=10, max_length=200)


class GoogleStatusOut(BaseModel):
    """Lets the login page know whether to offer Google sign-in at all."""

    enabled: bool


class AccountOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    learner_id: int | None = None
    created_at: datetime


class AuthTokenOut(BaseModel):
    """Bearer token plus the account it belongs to."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Token lifetime in seconds.")
    account: AccountOut
    learner_id: int | None = Field(
        default=None,
        description="Learner record to personalise the dashboard, once linked.",
    )
