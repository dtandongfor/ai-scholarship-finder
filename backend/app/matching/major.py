from ..matching.utils import is_valid_value


def check_major(student, scholarship):

    if not is_valid_value(student.major):
        return {
            "matched": False,
            "points": 0
        }

    if not is_valid_value(scholarship.major):
        return {
            "matched": False,
            "points": 0
        }

    student_major = student.major.strip().lower()
    scholarship_major = scholarship.major.strip().lower()

    if student_major == scholarship_major:

        return {
            "matched": True,
            "points": 25,
            "details": [
                f"{student.major} matches the scholarship requirement."
            ]
        }

    return {
        "matched": False,
        "points": 0
    }