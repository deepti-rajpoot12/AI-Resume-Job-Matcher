from pydantic import BaseModel, Field


class ResumeAnalysis(BaseModel):
    """Validated data returned by the LLM for one resume and job description."""

    match_score: int = Field(ge=0, le=100)
    matching_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    improvement_suggestions: list[str]
    interview_questions: list[str]


class AnalysisResponse(BaseModel):
    success: bool = True
    analysis: ResumeAnalysis
