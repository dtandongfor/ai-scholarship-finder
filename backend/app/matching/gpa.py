def check_gpa(student, scholarship):

    if not student.gpa or not scholarship.gpa_requirement:
        return {
            "matched": False,
            "points": 0
        }

    try:
        student_gpa = float(student.gpa)
        required_gpa = float(scholarship.gpa_requirement)

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