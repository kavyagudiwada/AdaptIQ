"""Initial assessment endpoints."""

from fastapi import APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import DbSession
from app.schemas.assessment import (
    AssessmentGenerateRequest,
    AssessmentPaperOut,
    AssessmentResultOut,
    AssessmentSubmitRequest,
)
from app.services.assessment_service import generate_paper, submit_assessment

router = APIRouter(prefix="/assessment", tags=["assessment"])


@router.post(
    "/generate", response_model=AssessmentPaperOut, status_code=status.HTTP_200_OK
)
async def generate(
    payload: AssessmentGenerateRequest, session: DbSession
) -> AssessmentPaperOut:
    """Generate a short diagnostic quiz personalised to the learner."""
    return await generate_paper(session, payload.learner_id)


@router.post("/submit", response_model=AssessmentResultOut)
async def submit(
    payload: AssessmentSubmitRequest, session: DbSession
) -> AssessmentResultOut:
    """Grade the assessment, analyse it and persist the result."""
    return await submit_assessment(session, payload)
