import asyncio
import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app.models.analysis import AnalysisResponse
from app.services.llm import LlmConfigurationError, LlmServiceError, analyze_resume
from app.services.pdf_parser import PdfExtractionError, extract_text_from_pdf
from app.services.history import save_analysis

router = APIRouter(prefix="/api", tags=["analysis"])
logger = logging.getLogger(__name__)


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    resume: UploadFile | None = File(default=None),
    job_description: str = Form(default=""),
) -> AnalysisResponse:
    """Extract a resume PDF and compare it to a job description with an LLM."""
    if resume is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A resume PDF is required.")

    filename = resume.filename or ""
    is_pdf = resume.content_type == "application/pdf" or filename.lower().endswith(".pdf")
    if not is_pdf:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please upload a PDF resume.")

    if not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A job description is required.",
        )

    pdf_bytes = await resume.read()
    try:
        resume_text = extract_text_from_pdf(pdf_bytes)
    except PdfExtractionError as error:
        logger.exception("PDF extraction failed for /api/analyze")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error

    try:
        analysis_result = await asyncio.to_thread(analyze_resume, resume_text, job_description.strip())
    except LlmConfigurationError as error:
        logger.exception("Gemini configuration failed for /api/analyze")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is not configured. Add GEMINI_API_KEY to backend/.env.",
        ) from error
    except LlmServiceError as error:
        logger.exception("Gemini analysis failed for /api/analyze")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The AI analysis service could not complete your request. Please try again.",
        ) from error

    try:
        await asyncio.to_thread(save_analysis, analysis_result, job_description.strip(), filename or None)
    except Exception:
        logger.exception("Analysis history persistence failed")
    return AnalysisResponse(analysis=analysis_result)
