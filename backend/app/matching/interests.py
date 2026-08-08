from app.matching.utils import (
    is_valid_value,
    normalize_list,
    requirement_match_ratio,
)
from app.matching.knowledge import INTEREST_SYNONYMS


def check_interests(student, scholarship):

    if not is_valid_value(student.interests):
        return {
            "matched": False,
            "points": 0
        }

    if not is_valid_value(scholarship.interests):
        return {
            "matched": False,
            "points": 0
        }

    student_items = normalize_list(student.interests)
    scholarship_items = normalize_list(scholarship.interests)

    match_ratio, matches = requirement_match_ratio(
        student_items,
        scholarship_items,
        INTEREST_SYNONYMS,
    )

    if matches:

        return {
            "matched": True,
            "match_ratio": match_ratio,
            "details": [
                f"{student_match.title()} matches the scholarship interest "
                f"{scholarship_match.title()}."
                for student_match, scholarship_match in matches
            ]
        }

    return {
        "matched": False,
        "points": 0
    }


