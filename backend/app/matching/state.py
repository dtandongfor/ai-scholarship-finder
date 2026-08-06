def check_state(student, scholarship):

    if not student.state or not scholarship.state:
        return {
            "matched": False,
            "points": 0
        }

    if student.state.lower().strip() == scholarship.state.lower().strip():
        return {
            "matched": True,
            "points": 10
        }

    return {
        "matched": False,
        "points": 0
    }