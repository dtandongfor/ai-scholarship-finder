from .knowledge import SKILL_SYNONYMS
from .utils import normalize_list, semantic_match


def check_skills(student, scholarship):

    # ==========================================
    # NO SCHOLARSHIP SKILL REQUIREMENT
    # ==========================================

    if not scholarship.skills:

        return {
            "matched": False,
            "points": 0,
            "details": []
        }

    # ==========================================
    # STUDENT HAS NO SKILLS
    # ==========================================

    if not student.skills:

        return {
            "matched": False,
            "points": 0,
            "details": []
        }

    # ==========================================
    # NORMALIZE SKILLS
    # ==========================================

    student_skills = normalize_list(
        student.skills
    )

    scholarship_skills = normalize_list(
        scholarship.skills
    )

    # ==========================================
    # FIND SEMANTIC MATCH
    # ==========================================

    matched, student_match, scholarship_match = semantic_match(
        student_skills,
        scholarship_skills,
        SKILL_SYNONYMS
    )

    # ==========================================
    # MATCH FOUND
    # ==========================================

    if matched:

        return {
            "matched": True,
            "points": 0,
            "details": [
                f"{student_match.title()} matches "
                f"the required skill "
                f"{scholarship_match.title()}."
            ]
        }

    # ==========================================
    # NO MATCH
    # ==========================================

    return {
        "matched": False,
        "points": 0,
        "details": []
    }




