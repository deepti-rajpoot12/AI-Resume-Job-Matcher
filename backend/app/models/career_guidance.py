from pydantic import BaseModel, Field

from app.models.analysis import ResumeAnalysis


class CareerGuidanceRequest(BaseModel):
    analysis: ResumeAnalysis
    job_description: str = Field(min_length=1, max_length=20_000)


class PrioritySkill(BaseModel):
    skill: str
    reason: str


class SkillExplanation(BaseModel):
    skill: str
    explanation: str


class LearningResource(BaseModel):
    title: str
    url: str


class ActionableSkillPlan(BaseModel):
    skill: str
    priority: str = Field(pattern="^(High|Medium|Low)$")
    why_it_matters: str
    recommended_topics: list[str]
    recommended_resources: list[LearningResource]
    practical_exercise: str
    interview_focus: str
    estimated_effort: str


class CareerGuidance(BaseModel):
    priority_skills: list[PrioritySkill]
    learning_path: list[str]
    skill_explanations: list[SkillExplanation]
    recommended_topics: list[str]
    interview_focus: list[str]
    skill_plans: list[ActionableSkillPlan] = Field(default_factory=list)


class CareerGuidanceResponse(BaseModel):
    success: bool = True
    guidance: CareerGuidance
