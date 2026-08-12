from app.matching.utils import is_valid_value
from .eligibility import normalize_state


def check_state(student, scholarship):

    if not is_valid_value(student.state):
        return {
            "matched": False,
            "points": 0
        }

    if not is_valid_value(scholarship.state):
        return {
            "matched": False,
            "points": 0
        }

    student_state = normalize_state(student.state)
    scholarship_state = normalize_state(scholarship.state)

    if student_state == scholarship_state:

        return {
            "matched": True,
            "points": 10,
            "details": [
                f"{student.state} matches the scholarship state requirement."
            ]
        }

    return {
        "matched": False,
        "points": 0
    }
