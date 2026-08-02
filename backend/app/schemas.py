from pydantic import BaseModel


class ScholarshipBase(BaseModel):
    name: str
    provider: str
    amount: str | None = None
    deadline: str | None = None
    major: str | None = None
    gpa_requirement: str | None = None
    eligibility: str | None = None


class ScholarshipCreate(ScholarshipBase):
    pass


class Scholarship(ScholarshipBase):
    id: int

    class Config:
        from_attributes = True