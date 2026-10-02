"""Adaptive quiz endpoints."""

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DbSession
from app.schemas.quiz import (
    QuizGenerateRequest,
    QuizOut,
    QuizResultOut,
    QuizSubmitRequest,
)
from app.services.quiz_service import generate_quiz, submit_quiz

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/generate", response_model=QuizOut)
async def generate(payload: QuizGenerateRequest, session: DbSession) -> QuizOut:
    """Generate a practice set at the difficulty this learner needs right now."""
    return await generate_quiz(session, payload)


@router.post("/submit", response_model=QuizResultOut)
async def submit(payload: QuizSubmitRequest, session: DbSession) -> QuizResultOut:
    """Grade the attempt, store it and report the adapted difficulty."""
    return await submit_quiz(session, payload)
