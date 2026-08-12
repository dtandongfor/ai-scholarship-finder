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
    eligible_student_types = Column(String)
    max_household_income = Column(Integer)
    min_sat_score = Column(Integer)
    min_act_score = Column(Integer)

    weights = Column(JSON)

    # Keep enough source information to verify and refresh imported data.
    source_name = Column(String)
    source_id = Column(String)
    source_url = Column(String)
    application_url = Column(String)
    description = Column(String)
    requirements_raw = Column(String)
    requirements = Column(JSON)
    requirements_complete = Column(Boolean, nullable=False, default=False)
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
    affiliations = Column(String)
    demonstrated_financial_need = Column(Boolean)
    planned_term_credits = Column(Integer)
    student_type = Column(String)
    household_income = Column(Integer)
    sat_score = Column(Integer)
    act_score = Column(Integer)
    financial_aid_submitted = Column(Boolean)
    pell_eligible = Column(Boolean)
    enrollment_status = Column(String)
    completed_credits = Column(Integer)
    volunteer_hours = Column(Integer)
    work_hours = Column(Integer)
    disciplinary_good_standing = Column(Boolean)
    accepts_service_commitment = Column(Boolean)
    is_first_generation = Column(Boolean)
    eligible_for_women_tech_scholarships = Column(Boolean)
    can_seek_security_clearance = Column(Boolean)


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    comment = Column(String)
    created_at = Column(DateTime)
