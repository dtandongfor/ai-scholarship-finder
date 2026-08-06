from .knowledge import SKILL_SYNONYMS
from .utils import normalize_list, semantic_match


def check_skills(student, scholarship):

    if not scholarship.skills:
        return {
            "matched": True,
            "points": 1,
            "details": ["No skill requirement."]
        }

    student_skills = normalize_list(student.skills)
    scholarship_skills = normalize_list(scholarship.skills)

    matched, student_match, scholarship_match = semantic_match(
        student_skills,
        scholarship_skills,
        SKILL_SYNONYMS
    )

    if matched:
        return {
            "matched": True,
            "points": 1,
            "details": [
                f"{student_match.title()} satisfies {scholarship_match.title()}."
            ]
        }

    return {
        "matched": False,
        "points": 1,
        "details": [
            "Required skills not found."
        ]
    }

