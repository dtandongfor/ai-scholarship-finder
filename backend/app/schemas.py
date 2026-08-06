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

class ScholarshipCreate(ScholarshipBase):
    pass


class ScholarshipUpdate(ScholarshipBase):
    pass


class Scholarship(ScholarshipBase):
    id: int

    class Config:
        from_attributes = True

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
    points: int
    details: list[str] = []

class RecommendationMatch(BaseModel):
    score: int
    raw_score: int
    matched_on: list[str]
    explanations: list
    summary: str
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