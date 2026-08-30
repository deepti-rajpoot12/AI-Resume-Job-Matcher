from datetime import datetime

from pydantic import BaseModel

from app.models.analysis import ResumeAnalysis
from app.models.career_guidance import CareerGuidance


class HistorySummary(BaseModel):
    id: int
    created_at: datetime
    target_role: str
    match_score: int
    matching_skill_count: int
    skill_gap_count: int


class HistoryDetail(HistorySummary):
    job_description: str
    resume_name: str | None = None
    analysis: ResumeAnalysis
    career_plan: CareerGuidance | None = None
