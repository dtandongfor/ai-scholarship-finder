from app.matching.utils import is_valid_value


def check_interests(student, scholarship):

    if not is_valid_value(student.interests):
        return {
            "matched": False,
            "points": 0
        }

    if not is_valid_value(scholarship.interests):
        return {
            "matched": False,
            "points": 0
        }

    student_interests = student.interests.lower()
    scholarship_interests = scholarship.interests.lower()

    student_items = [
        item.strip()
        for item in student_interests.split(",")
        if item.strip()
    ]

    scholarship_items = [
        item.strip()
        for item in scholarship_interests.split(",")
        if item.strip()
    ]

    matches = [
        item
        for item in scholarship_items
        if any(
            item in student_item
            or student_item in item
            for student_item in student_items
        )
    ]

    if matches:

        return {
            "matched": True,
            "points": 15,
            "details": [
                f"{match.title()} matches {match.title()}."
                for match in matches
            ]
        }

    return {
        "matched": False,
        "points": 0
    }


