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
    scholarship: Scholarship


class RecommendationResponse(BaseModel):
    student: str
    matches_found: int
    matches: list[RecommendationMatch]

