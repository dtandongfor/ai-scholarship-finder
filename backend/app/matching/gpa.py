def check_gpa(student, scholarship):

    try:
        student_gpa = float(student.gpa)
        required_gpa = float(scholarship.gpa_requirement)

        if student_gpa >= required_gpa:
            return {
                "matched": True,
                "points": 20
            }

    except (ValueError, TypeError):
        pass

    return {
        "matched": False,
        "points": 0
    }