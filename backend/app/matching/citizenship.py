def check_citizenship(student, scholarship):

    if not student.citizenship or not scholarship.citizenship:
        return {
            "matched": False,
            "points": 0
        }

    if student.citizenship.lower().strip() == scholarship.citizenship.lower().strip():
        return {
            "matched": True,
            "points": 10
        }

    return {
        "matched": False,
        "points": 0
    }