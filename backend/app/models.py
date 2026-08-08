from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String
from .database import Base


class Scholarship(Base):
    __tablename__ = "scholarships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    amount = Column(String)
    deadline = Column(String)
    major = Column(String)
    gpa_requirement = Column(String)

    eligibility = Column(String)

    state = Column(String)
    citizenship = Column(String)

    interests = Column(String)

    skills = Column(String)
    projects = Column(String)
    leadership = Column(String)
    volunteer = Column(String)
    certifications = Column(String)

    weights = Column(JSON)

    # Keep enough source information to verify and refresh imported data.
    source_name = Column(String)
    source_id = Column(String)
    source_url = Column(String)
    application_url = Column(String)
    description = Column(String)
    requirements_raw = Column(String)
    last_verified_at = Column(DateTime)
    is_active = Column(Boolean, nullable=False, default=True)
    


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    major = Column(String)
    gpa = Column(String)
    year = Column(String)
    university = Column(String)

    state = Column(String)
    citizenship = Column(String)
    interests = Column(String)

    skills = Column(String)
    projects = Column(String)
    leadership = Column(String)
    volunteer = Column(String)
    certifications = Column(String)
    languages = Column(String)
    awards = Column(String)
