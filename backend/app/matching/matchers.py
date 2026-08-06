from .major import check_major
from .gpa import check_gpa
from .state import check_state
from .citizenship import check_citizenship
from .interests import check_interests
from .skills import check_skills
from .projects import check_projects
from .leadership import check_leadership
from .volunteer import check_volunteer
from .certifications import check_certifications


MATCHERS = {
    "major": check_major,
    "gpa": check_gpa,
    "state": check_state,
    "citizenship": check_citizenship,
    "interests": check_interests,
    "skills": check_skills,
    "projects": check_projects,
    "leadership": check_leadership,
    "volunteer": check_volunteer,
    "certifications": check_certifications,
}