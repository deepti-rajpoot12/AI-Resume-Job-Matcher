"""Deterministic, bounded context assembly for Gemini requests.

Priority order: system instructions, candidate evidence, job requirements, identified skill gaps,
retrieved knowledge, then task instructions. Knowledge is never treated as candidate evidence.
"""

from app.models.analysis import ResumeAnalysis
from app.prompts.resources import resources_for_skills
from app.services.retrieval import RetrievedKnowledge

MAX_RESUME_CHARS = 18_000
MAX_JOB_DESCRIPTION_CHARS = 10_000
MAX_RETRIEVED_CHUNKS = 6
MAX_RETRIEVED_CHARS = 7_500


def _trim(text: str, limit: int) -> str:
    text = text.strip()
    return text if len(text) <= limit else f"{text[:limit].rsplit(' ', 1)[0]}…"


def build_resume_analysis_context(resume_text: str, job_description: str) -> str:
    return "\n\n".join((
        "## RESUME EVIDENCE\n" + _trim(resume_text, MAX_RESUME_CHARS),
        "## JOB REQUIREMENTS\n" + _trim(job_description, MAX_JOB_DESCRIPTION_CHARS),
        "## TASK\nCompare the resume evidence to job requirements and produce the validated analysis.",
    ))


def clean_retrieved_context(knowledge: list[RetrievedKnowledge]) -> tuple[str, int]:
    cleaned: list[str] = []
    seen: set[str] = set()
    used_chars = 0
    for item in knowledge[:MAX_RETRIEVED_CHUNKS]:
        text = " ".join(item.text.split())
        if not text or text in seen:
            continue
        remaining = MAX_RETRIEVED_CHARS - used_chars
        if remaining <= 0:
            break
        seen.add(text)
        content = _trim(text, remaining)
        metadata = item.metadata
        relevance = "unknown" if item.distance is None else f"{1 - item.distance:.2f}"
        cleaned.append(
            f"[Knowledge {len(cleaned) + 1}]\nSkill: {metadata.get('skill', 'Unknown')}\n"
            f"Topic: {metadata.get('topic', 'career-development')}\nRelevance: {relevance}\nContent: {content}"
        )
        used_chars += len(content)
    return "\n\n".join(cleaned) or "No relevant local knowledge was retrieved.", len(cleaned)


def build_career_guidance_context(analysis: ResumeAnalysis, job_description: str, knowledge: list[RetrievedKnowledge]) -> tuple[str, int]:
    retrieved_context, chunk_count = clean_retrieved_context(knowledge)
    context = "\n\n".join((
        "## CANDIDATE PROFILE\n" + analysis.model_dump_json(),
        "## JOB REQUIREMENTS\n" + _trim(job_description, MAX_JOB_DESCRIPTION_CHARS),
        "## IDENTIFIED SKILL GAPS\n" + (", ".join(analysis.missing_skills) or "No skill gaps identified."),
        "## RETRIEVED KNOWLEDGE\n" + retrieved_context,
        "## TRUSTED LEARNING RESOURCES\n" + resources_for_skills(analysis.missing_skills),
        "## TASK\nGenerate an ordered, concise roadmap and one actionable plan per important gap. Candidate facts may only come from the candidate profile; learning facts may only come from retrieved knowledge. Include a resource URL only when it appears in Trusted Learning Resources.",
    ))
    return context, chunk_count
