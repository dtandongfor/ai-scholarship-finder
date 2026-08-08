from app.matching.utils import is_valid_value


STOP_WORDS = {
    "project",
    "projects",
    "work",
    "experience",
    "research",
    "application",
    "app",
    "program",
    "programs",
}


def normalize_project_text(value):
    if not is_valid_value(value):
        return []

    words = []

    for word in str(value).lower().split():
        cleaned = word.strip(".,!?;:()[]{}")

        if cleaned and cleaned not in STOP_WORDS:
            words.append(cleaned)

    return words


def check_projects(student, scholarship):

    if not is_valid_value(student.projects):
        return {
            "matched": False,
            "points": 0,
            "details": []
        }

    if not is_valid_value(scholarship.projects):
        return {
            "matched": True,
            "points": 5,
            "details": [
                "No project requirement."
            ]
        }

    student_text = str(student.projects).lower()
    scholarship_text = str(scholarship.projects).lower()

    # ==========================================
    # EXACT PHRASE MATCH
    # ==========================================

    if scholarship_text in student_text:
        return {
            "matched": True,
            "points": 5,
            "details": [
                scholarship.projects
            ]
        }

    # ==========================================
    # MEANINGFUL KEYWORD MATCH
    # ==========================================

    student_words = set(
        normalize_project_text(
            student.projects
        )
    )

    scholarship_words = set(
        normalize_project_text(
            scholarship.projects
        )
    )

    if not scholarship_words:
        return {
            "matched": False,
            "points": 0,
            "details": []
        }

    matched_words = (
        student_words.intersection(
            scholarship_words
        )
    )

    # Require at least one meaningful project keyword.
    if matched_words:
        return {
            "matched": True,
            "points": 5,
            "details": [
                scholarship.projects
            ]
        }

    return {
        "matched": False,
        "points": 0,
        "details": []
    }

