from .utils import is_valid_value


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

    student_citizenship = student.citizenship.strip().lower()
    scholarship_citizenship = scholarship.citizenship.strip().lower()

    if student_citizenship == scholarship_citizenship:
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