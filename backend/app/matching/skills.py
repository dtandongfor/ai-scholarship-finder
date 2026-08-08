from .knowledge import SKILL_SYNONYMS
from .utils import normalize_list, requirement_match_ratio


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

    match_ratio, matches = requirement_match_ratio(
        student_skills,
        scholarship_skills,
        SKILL_SYNONYMS
    )

    # ==========================================
    # MATCH FOUND
    # ==========================================

    if matches:

        return {
            "matched": True,
            "match_ratio": match_ratio,
            "details": [
                f"{student_match.title()} matches "
                f"the required skill "
                f"{scholarship_match.title()}."
                for student_match, scholarship_match in matches
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




