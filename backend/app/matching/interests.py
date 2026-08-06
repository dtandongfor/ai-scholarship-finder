from .knowledge import INTEREST_SYNONYMS
from .utils import normalize_list, semantic_match


def check_interests(student, scholarship):

    if not scholarship.interests:
        return {
            "matched": True,
            "points": 1,
            "details": ["No interest requirement."]
        }

    student_interests = normalize_list(student.interests)
    scholarship_interests = normalize_list(scholarship.interests)

    matched, student_match, scholarship_match = semantic_match(
        student_interests,
        scholarship_interests,
        INTEREST_SYNONYMS
    )

    if matched:
        return {
            "matched": True,
            "points": 1,
            "details": [
                f"{student_match.title()} matches {scholarship_match.title()}."
            ]
        }

    return {
        "matched": False,
        "points": 1,
        "details": [
            "No related interests found."
        ]
    }



