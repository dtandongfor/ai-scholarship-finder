from .utils import normalize_list


VOLUNTEER_SYNONYMS = {
    "tutoring": [
        "tutor",
        "tutoring",
        "academic tutor",
        "stem tutor",
        "stem tutoring"
    ],

    "mentoring": [
        "mentor",
        "mentoring",
        "mentorship"
    ],

    "community service": [
        "community service",
        "community outreach",
        "outreach"
    ],

    "food assistance": [
        "food bank",
        "food pantry",
        "food drive"
    ],

    "nonprofit": [
        "nonprofit",
        "non-profit",
        "charity"
    ]
}


def normalize_text(value):
    """
    Normalize text for comparison.
    """
    if not value:
        return ""

    return " ".join(
        value.lower()
        .replace(",", " ")
        .replace(".", " ")
        .replace("-", " ")
        .split()
    )


def check_volunteer(student, scholarship):

    if not student.volunteer:
        return {
            "matched": False,
            "points": 0,
            "details": []
        }

    if not scholarship.volunteer:
        return {
            "matched": False,
            "points": 0,
            "details": []
        }

    student_text = normalize_text(student.volunteer)
    scholarship_text = normalize_text(scholarship.volunteer)

    # ------------------------------------------
    # 1. EXACT MATCH
    # ------------------------------------------

    if student_text == scholarship_text:
        return {
            "matched": True,
            "points": 1,
            "details": [
                f"{student.volunteer} matches the volunteer requirement."
            ]
        }

    # ------------------------------------------
    # 2. MEANINGFUL PHRASE MATCH
    # ------------------------------------------

    for category, synonyms in VOLUNTEER_SYNONYMS.items():

        student_matches = []
        scholarship_matches = []

        for synonym in synonyms:

            synonym = normalize_text(synonym)

            if synonym in student_text:
                student_matches.append(synonym)

            if synonym in scholarship_text:
                scholarship_matches.append(synonym)

        if student_matches and scholarship_matches:

            return {
                "matched": True,
                "points": 1,
                "details": [
                    f"{student.volunteer} aligns with "
                    f"{scholarship.volunteer}."
                ]
            }

    # ------------------------------------------
    # 3. NO MATCH
    # ------------------------------------------

    return {
        "matched": False,
        "points": 0,
        "details": []
    }



