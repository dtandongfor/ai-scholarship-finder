from .knowledge import CERTIFICATION_GROUPS
from .utils import normalize_list, requirement_match_ratio


def certifications_match(student_cert, scholarship_cert):
    if student_cert == scholarship_cert:
        return True

    for group_name, group_values in CERTIFICATION_GROUPS.items():
        group_terms = [group_name.lower(), *map(str.lower, group_values)]

        student_in_group = any(term in student_cert for term in group_terms)
        scholarship_in_group = any(
            term in scholarship_cert
            for term in group_terms
        )

        if student_in_group and scholarship_in_group:
            return True

    return False


def check_certifications(student, scholarship):

    # No scholarship certification requirement
    if not scholarship.certifications:
        return {
            "matched": False,
            "points": 0,
            "details": []
        }

    # Student has no certifications
    if not student.certifications:
        return {
            "matched": False,
            "points": 0,
            "details": []
        }

    student_certs = normalize_list(
        student.certifications
    )

    scholarship_certs = normalize_list(
        scholarship.certifications
    )

    match_ratio, matched_pairs = requirement_match_ratio(
        student_certs,
        scholarship_certs,
        match_function=certifications_match,
    )

    if matched_pairs:
        return {
            "matched": True,
            "match_ratio": match_ratio,
            "details": [
                f"{student_cert.title()} matches the required certification "
                f"{scholarship_cert.title()}."
                for student_cert, scholarship_cert in matched_pairs
            ]
        }

    return {
        "matched": False,
        "points": 0,
        "details": []
    }

