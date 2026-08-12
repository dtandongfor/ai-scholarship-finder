import re


def parse_gpa(value):
    """Extract a numeric GPA from a published requirement string."""

    match = re.search(r"\d(?:\.\d+)?", str(value))
    return float(match.group()) if match else None


def check_gpa(student, scholarship):

    if not student.gpa or not scholarship.gpa_requirement:
        return {
            "matched": False,
            "points": 0
        }

    try:
        student_gpa = parse_gpa(student.gpa)
        required_gpa = parse_gpa(scholarship.gpa_requirement)
        if student_gpa is None or required_gpa is None:
            raise ValueError

    except (ValueError, TypeError):
        return {
            "matched": False,
            "points": 0
        }

    if student_gpa >= required_gpa:
        return {
            "matched": True,
            "points": 20,
            "details": [
                f"GPA {student_gpa:.2f} meets the required GPA of {required_gpa:.2f}."
            ]
        }

    return {
        "matched": False,
        "points": 0,
        "details": [
            f"GPA {student_gpa:.2f} is below the required GPA of {required_gpa:.2f}."
        ]
    }
