import os
import logging
import time

from google import genai
from google.genai import errors

from app.models.analysis import ResumeAnalysis
from app.models.career_guidance import CareerGuidance
from app.prompts.career_guidance import CAREER_GUIDANCE_PROMPT_VERSION, CAREER_GUIDANCE_SYSTEM_PROMPT
from app.prompts.context import build_career_guidance_context
from app.prompts.resources import trusted_url
from app.services.llm import LlmConfigurationError, LlmServiceError
from app.services.retrieval import RetrievedKnowledge

logger = logging.getLogger(__name__)


def generate_career_guidance(
    analysis: ResumeAnalysis,
    job_description: str,
    knowledge: list[RetrievedKnowledge],
) -> CareerGuidance:
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")
    if not api_key:
        raise LlmConfigurationError("GEMINI_API_KEY is not configured.")
    if not model:
        raise LlmConfigurationError("GEMINI_MODEL is not configured.")

    prompt, retrieved_chunk_count = build_career_guidance_context(analysis, job_description, knowledge)
    started_at = time.perf_counter()
    try:
        client = genai.Client(api_key=api_key)
        interaction = client.interactions.create(
            model=model,
            input=prompt,
            system_instruction=CAREER_GUIDANCE_SYSTEM_PROMPT,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": CareerGuidance.model_json_schema(),
            },
        )
        guidance = CareerGuidance.model_validate_json(interaction.output_text)
        guidance = guidance.model_copy(update={
            "skill_plans": [
                plan.model_copy(update={"recommended_resources": [
                    resource for resource in plan.recommended_resources if trusted_url(resource.url)
                ]})
                for plan in guidance.skill_plans
            ]
        })
        logger.info("gemini_task=career_guidance prompt_version=%s model=%s retrieved_chunks=%d context_chars=%d duration_ms=%d", CAREER_GUIDANCE_PROMPT_VERSION, model, retrieved_chunk_count, len(prompt), (time.perf_counter() - started_at) * 1000)
        return guidance
    except errors.APIError as error:
        raise LlmServiceError("Gemini could not generate career guidance.") from error
    except (AttributeError, TypeError, ValueError) as error:
        raise LlmServiceError("Gemini returned invalid career guidance.") from error
