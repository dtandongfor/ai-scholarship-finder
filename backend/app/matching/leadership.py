# app/matching/leadership.py

from .knowledge import LEADERSHIP_KEYWORDS


def check_leadership(student, scholarship):

    student_leadership = (
        str(student.leadership).strip().lower()
        if student.leadership
        else ""
    )

    scholarship_leadership = (
        str(scholarship.leadership).strip().lower()
        if scholarship.leadership
        else ""
    )

    # No scholarship requirement
    if not scholarship_leadership:
        return {
            "matched": True,
            "points": 3,
            "details": ["No leadership requirement."]
        }

    # Student has no leadership information
    if not student_leadership:
        return {
            "matched": False,
            "points": 0,
            "details": ["No leadership experience listed."]
        }

    # Look specifically for actual leadership roles
    matched_keyword = None

    for keyword in LEADERSHIP_KEYWORDS:
        if keyword in student_leadership:
            matched_keyword = keyword
            break

    if matched_keyword:

        return {
            "matched": True,
            "points": 3,
            "details": [
                f"{student.leadership}"
            ]
        }

    return {
        "matched": False,
        "points": 0,
        "details": [
            f"'{student.leadership}' does not indicate a leadership role."
        ]
    }