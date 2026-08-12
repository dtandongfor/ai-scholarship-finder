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
    scholarship_majors = {
        item.strip().lower()
        for item in scholarship.major.split(",")
        if item.strip()
    }

    if student_major in scholarship_majors:

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
