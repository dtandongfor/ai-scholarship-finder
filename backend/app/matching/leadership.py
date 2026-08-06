def check_leadership(student, scholarship):

    if not student.leadership or not scholarship.leadership:
        return {
            "matched": False,
            "points": 0
        }

    student_leadership = student.leadership.lower()
    scholarship_leadership = scholarship.leadership.lower()

    keywords = scholarship_leadership.split()

    matches = [
        word for word in keywords
        if word in student_leadership
    ]

    if matches:
        return {
            "matched": True,
            "points": 3,
            "details": matches
        }

    return {
        "matched": False,
        "points": 0
    }