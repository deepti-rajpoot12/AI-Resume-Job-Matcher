import os
import logging
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from app.models.analysis import ResumeAnalysis
from app.prompts.context import build_resume_analysis_context
from app.prompts.resume_analysis import RESUME_ANALYSIS_PROMPT_VERSION, RESUME_ANALYSIS_SYSTEM_PROMPT

load_dotenv()

logger = logging.getLogger(__name__)


class LlmConfigurationError(Exception):
    """Raised when required local LLM configuration is missing."""


class LlmServiceError(Exception):
    """Raised when Gemini cannot produce a valid analysis."""


def analyze_resume(resume_text: str, job_description: str) -> ResumeAnalysis:
    """Ask Gemini for a Pydantic-validated resume analysis."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise LlmConfigurationError("GEMINI_API_KEY is not configured.")

    model = os.getenv("GEMINI_MODEL")
    if not model:
        raise LlmConfigurationError("GEMINI_MODEL is not configured.")

    client = genai.Client(api_key=api_key)
    user_prompt = build_resume_analysis_context(resume_text, job_description)
    started_at = time.perf_counter()

    try:
        interaction = client.interactions.create(
            model=model,
            input=user_prompt,
            system_instruction=RESUME_ANALYSIS_SYSTEM_PROMPT,
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": ResumeAnalysis.model_json_schema(),
            },
        )
        analysis = ResumeAnalysis.model_validate_json(interaction.output_text)
        logger.info("gemini_task=resume_analysis prompt_version=%s model=%s context_chars=%d duration_ms=%d", RESUME_ANALYSIS_PROMPT_VERSION, model, len(user_prompt), (time.perf_counter() - started_at) * 1000)
    except errors.APIError as error:
        if error.code in (401, 403):
            message = "Gemini rejected the configured API key."
        elif error.code == 429:
            message = "Gemini free-tier quota is exhausted."
        elif error.code in (400, 404):
            message = "Gemini rejected the configured model or request."
        else:
            message = "Gemini could not complete the analysis request."
        raise LlmServiceError(message) from error
    except (AttributeError, TypeError, ValueError) as error:
        raise LlmServiceError("Gemini returned an invalid structured analysis.") from error

    if analysis is None:
        raise LlmServiceError("The AI service did not return an analysis.")

    return analysis
