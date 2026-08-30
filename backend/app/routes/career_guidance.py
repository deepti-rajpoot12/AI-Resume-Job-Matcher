import asyncio
import logging

from fastapi import APIRouter, HTTPException, status

from app.models.career_guidance import CareerGuidanceRequest, CareerGuidanceResponse
from app.services.career_guidance import generate_career_guidance
from app.services.llm import LlmConfigurationError, LlmServiceError
from app.services.retrieval import retrieve_career_knowledge
from app.services.vector_store import VectorStoreError, knowledge_base_ready
from app.services.history import attach_career_plan

router = APIRouter(prefix="/api", tags=["career guidance"])
logger = logging.getLogger(__name__)


@router.post("/career-guidance", response_model=CareerGuidanceResponse)
async def career_guidance(request: CareerGuidanceRequest) -> CareerGuidanceResponse:
    if not request.job_description.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A job description is required.")
    if request.analysis.missing_skills and not knowledge_base_ready():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Career knowledge is not ready. Build the local knowledge base first.",
        )
    try:
        knowledge = await asyncio.to_thread(retrieve_career_knowledge, request.analysis.missing_skills)
        guidance = await asyncio.to_thread(
            generate_career_guidance, request.analysis, request.job_description.strip(), knowledge
        )
        try:
            await asyncio.to_thread(attach_career_plan, request.analysis, guidance)
        except Exception:
            logger.exception("Career plan history persistence failed")
    except VectorStoreError as error:
        logger.exception("Career knowledge retrieval failed")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Career guidance is unavailable.") from error
    except LlmConfigurationError as error:
        logger.exception("Gemini configuration failed for career guidance")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="The AI service is not configured.") from error
    except LlmServiceError as error:
        logger.exception("Gemini career guidance failed")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Career guidance could not be generated. Please try again.") from error
    return CareerGuidanceResponse(guidance=guidance)
