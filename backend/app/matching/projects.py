def check_projects(student, scholarship):

    if not student.projects or not scholarship.projects:
        return {
            "matched": False,
            "points": 0
        }

    student_projects = student.projects.lower()
    scholarship_projects = scholarship.projects.lower()

    keywords = scholarship_projects.split()

    matches = [
        word for word in keywords
        if word in student_projects
    ]

    if matches:
        return {
            "matched": True,
            "points": 5,
            "details": matches
        }

    return {
        "matched": False,
        "points": 0
    }