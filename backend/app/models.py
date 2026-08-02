from sqlalchemy import Column, Integer, String
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