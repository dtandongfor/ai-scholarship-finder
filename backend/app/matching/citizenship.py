from .utils import is_valid_value
from .eligibility import citizenship_matches


def check_citizenship(student, scholarship):

    if not is_valid_value(student.citizenship):
        return {
            "matched": False,
            "points": 0
        }

    if not is_valid_value(scholarship.citizenship):
        return {
            "matched": False,
            "points": 0
        }

    if citizenship_matches(student.citizenship, scholarship.citizenship):
        return {
            "matched": True,
            "points": 10,
            "details": [
                f"{student.citizenship} matches the scholarship citizenship requirement."
            ]
        }

    return {
        "matched": False,
        "points": 0
    }
