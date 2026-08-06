def check_certifications(student, scholarship):

    if not student.certifications or not scholarship.certifications:
        return {
            "matched": False,
            "points": 0
        }

    student_certifications = [
        item.strip().lower()
        for item in student.certifications.split(",")
    ]

    scholarship_certifications = [
        item.strip().lower()
        for item in scholarship.certifications.split(",")
    ]

    matches = set(student_certifications).intersection(
        set(scholarship_certifications)
    )

    if matches:
        return {
            "matched": True,
            "points": 1,
            "details": list(matches)
        }

    return {
        "matched": False,
        "points": 0
    }