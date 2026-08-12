from datetime import datetime

from typing import Any, Literal

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
    eligible_student_types: str | None = None
    max_household_income: int | None = None
    min_sat_score: int | None = None
    min_act_score: int | None = None
    weights: dict[str, int] | None = None

    # Source-tracking fields used by the future data-ingestion pipeline.
    source_name: str | None = None
    source_id: str | None = None
    source_url: str | None = None
    application_url: str | None = None
    description: str | None = None
    requirements_raw: str | None = None
    requirements: dict[str, Any] | None = None
    requirements_complete: bool = False
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


class ScholarshipBatchIngestRequest(BaseModel):
    """A reviewed set of scholarship records from one public source."""

    scholarships: list[ScholarshipIngestRequest]


class ScholarshipBatchIngestResponse(BaseModel):
    created: int
    updated: int
    scholarships: list[Scholarship]


class ScholarshipSource(BaseModel):
    id: str
    name: str
    kind: Literal["university", "open_database", "directory"]
    country: str
    state: str | None = None
    url: str
    import_method: Literal[
        "reviewed_manual",
        "discovery_only",
        "enrichment_only",
    ]
    notes: str


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
    affiliations: str | None = None
    demonstrated_financial_need: bool | None = None
    planned_term_credits: int | None = None
    student_type: Literal["first_year", "transfer", "current", "graduate"] | None = None
    household_income: int | None = None
    sat_score: int | None = None
    act_score: int | None = None
    financial_aid_submitted: bool | None = None
    pell_eligible: bool | None = None
    enrollment_status: Literal["full_time", "part_time"] | None = None
    completed_credits: int | None = None
    volunteer_hours: int | None = None
    work_hours: int | None = None
    disciplinary_good_standing: bool | None = None
    accepts_service_commitment: bool | None = None
    is_first_generation: bool | None = None
    eligible_for_women_tech_scholarships: bool | None = None
    can_seek_security_clearance: bool | None = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True


class ResumePrefillResponse(BaseModel):
    """Fields suggested from a resume; the student must review them before saving."""

    suggestions: dict[str, str]
    review_notes: list[str]


class StudentDeletionRequest(BaseModel):
    """Email confirmation prevents an ID alone from deleting a profile."""

    email: str


class FeedbackCreate(BaseModel):
    rating: int
    category: Literal["useful", "incorrect_match", "missing_scholarship", "other"]
    comment: str | None = None


class FeedbackResponse(BaseModel):
    id: int
    message: str

class MatchExplanation(BaseModel):
    category: str
    points: float
    details: list[str] = []

class RecommendationMatch(BaseModel):
    score: int
    raw_score: float
    eligible: bool
    ineligibility_reasons: list[str]
    review_items: list[str]
    unassessed_requirements: list[str]
    application_checklist: list[str]
    selection_notes: list[str]
    match_level: str
    match_status: str
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
