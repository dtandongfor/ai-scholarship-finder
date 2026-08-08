from datetime import datetime

from typing import Literal

from pydantic import BaseModel


class ScholarshipBase(BaseModel):
    name: str
    provider: str
    amount: str | None = None
    deadline: str | None = None
    major: str | None = None
    gpa_requirement: str | None = None
    eligibility: str | None = None
    state: str | None = None
    citizenship: str | None = None
    interests: str | None = None

    skills: str | None = None
    projects: str | None = None
    leadership: str | None = None
    volunteer: str | None = None
    certifications: str | None = None
    weights: dict[str, int] | None = None

    # Source-tracking fields used by the future data-ingestion pipeline.
    source_name: str | None = None
    source_id: str | None = None
    source_url: str | None = None
    application_url: str | None = None
    description: str | None = None
    requirements_raw: str | None = None
    last_verified_at: datetime | None = None
    is_active: bool = True

class ScholarshipCreate(ScholarshipBase):
    pass


class ScholarshipUpdate(ScholarshipBase):
    pass


class Scholarship(ScholarshipBase):
    id: int

    class Config:
        from_attributes = True


class ScholarshipIngestRequest(ScholarshipBase):
    """A scholarship record received from a source or parser."""

    source_name: str


class ScholarshipIngestResponse(BaseModel):
    action: Literal["created", "updated"]
    scholarship: Scholarship


class ScholarshipParseRequest(BaseModel):
    source_name: str
    description: str
    source_id: str | None = None
    source_url: str | None = None
    application_url: str | None = None


class ScholarshipParsedData(BaseModel):
    name: str | None = None
    provider: str | None = None
    amount: str | None = None
    deadline: str | None = None
    major: str | None = None
    gpa_requirement: str | None = None
    eligibility: str | None = None
    state: str | None = None
    citizenship: str | None = None
    interests: str | None = None
    skills: str | None = None
    projects: str | None = None
    leadership: str | None = None
    volunteer: str | None = None
    certifications: str | None = None
    requirements_raw: str | None = None


class ScholarshipParseResponse(BaseModel):
    parsed: ScholarshipParsedData
    source_name: str
    source_id: str | None = None
    source_url: str | None = None
    application_url: str | None = None
    description: str
    ready_to_ingest: bool
    missing_required_fields: list[str]

class StudentBase(BaseModel):
    name: str
    email: str
    major: str
    gpa: str
    year: str
    university: str
    state: str
    citizenship: str
    interests: str

    # New recommendation fields
    skills: str | None = None
    projects: str | None = None
    leadership: str | None = None
    volunteer: str | None = None
    certifications: str | None = None
    languages: str | None = None
    awards: str | None = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

class MatchExplanation(BaseModel):
    category: str
    points: float
    details: list[str] = []

class RecommendationMatch(BaseModel):
    score: int
    raw_score: float
    eligible: bool
    ineligibility_reasons: list[str]
    match_level: str
    matched_on: list[str]
    explanations: list
    why_you_match: list[str]
    missing_requirements: list[str]
    application_tip: str
    scholarship: Scholarship


class RecommendationResponse(BaseModel):
    student: str
    matches_found: int
    matches: list[RecommendationMatch]

class ProfileAnalysisResponse(BaseModel):
    student: str
    profile_strength: int
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

    ai_summary: str 
    ai_advice: list[str] 
    improvement_plan: list[ImprovementItem]

class ImprovementItem(BaseModel):
    category: str
    scholarships: int
    reason: str
    action: str
 

class ProfileAnalysis(ProfileAnalysisResponse):
    pass

class ImprovementSimulationRequest(BaseModel):
    category: str
    value: str


class ImprovementSimulationResponse(BaseModel):
    improvement: str
    current_matches: int
    projected_matches: int
    increase: int

    current_average_score: int
    projected_average_score: int
    score_change: int

    impact: str

class DashboardResponse(BaseModel):
    student: str
    profile_strength: int
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    top_matches: list[RecommendationMatch]
    improvement_plan: list[ImprovementItem]
