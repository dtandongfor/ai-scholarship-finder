def check_projects(student, scholarship):

    if not student.projects or not scholarship.projects:
        return {
            "matched": False,
            "points": 0
        }

    student_projects = student.projects.strip().lower()
    scholarship_projects = scholarship.projects.strip().lower()

    if scholarship_projects in student_projects:
        return {
            "matched": True,
            "points": 5,
            "details": [
                scholarship.projects
            ]
        }

    student_words = set(student_projects.split())
    scholarship_words = set(scholarship_projects.split())

    matches = student_words.intersection(scholarship_words)

    if matches:
        return {
            "matched": True,
            "points": 5,
            "details": [
                scholarship.projects
            ]
        }

    return {
        "matched": False,
        "points": 0
    }