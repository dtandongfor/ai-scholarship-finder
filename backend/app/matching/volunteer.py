def check_volunteer(student, scholarship):

    if not student.volunteer or not scholarship.volunteer:
        return {
            "matched": False,
            "points": 0
        }

    student_volunteer = student.volunteer.lower()
    scholarship_volunteer = scholarship.volunteer.lower()

    keywords = scholarship_volunteer.split()

    matches = [
        word for word in keywords
        if word in student_volunteer
    ]

    if matches:
        return {
            "matched": True,
            "points": 1,
            "details": matches
        }

    return {
        "matched": False,
        "points": 0
    }