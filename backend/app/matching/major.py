from .knowledge import MAJOR_GROUPS


def check_major(student, scholarship):

    if not scholarship.major:
        return {
            "matched": True,
            "points": 1,
            "details": ["No major restriction."]
        }

    student_major = student.major.strip().lower()

    scholarship_majors = [
        major.strip().lower()
        for major in scholarship.major.split(",")
    ]

    # Exact major match
    if student_major in scholarship_majors:
        return {
            "matched": True,
            "points": 1,
            "details": [
                f"{student.major} matches the scholarship requirement."
            ]
        }

    # Group match (e.g. STEM, Business, Healthcare)
    for group in scholarship_majors:

        if group in MAJOR_GROUPS:

            if student_major in MAJOR_GROUPS[group]:

                return {
                    "matched": True,
                    "points": 1,
                    "details": [
                        f"{student.major} belongs to the {group.title()} field."
                    ]
                }

    return {
        "matched": False,
        "points": 1,
        "details": [
            f"{student.major} does not satisfy the major requirement."
        ]
    }

