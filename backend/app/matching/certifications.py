from .knowledge import CERTIFICATION_GROUPS
from .utils import normalize_list


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

    matches = []

    for scholarship_cert in scholarship_certs:

        for student_cert in student_certs:

            # ------------------------------------------
            # EXACT MATCH
            # ------------------------------------------

            if scholarship_cert == student_cert:
                matches.append(
                    f"{student_cert.title()} matches "
                    f"{scholarship_cert.title()}."
                )
                continue

            # ------------------------------------------
            # CERTIFICATION GROUP MATCH
            # ------------------------------------------

            for group_name, group_values in CERTIFICATION_GROUPS.items():

                group_values = [
                    value.lower()
                    for value in group_values
                ]

                scholarship_in_group = (
                    group_name.lower() in scholarship_cert
                    or any(
                        value in scholarship_cert
                        for value in group_values
                    )
                )

                student_in_group = (
                    group_name.lower() in student_cert
                    or any(
                        value in student_cert
                        for value in group_values
                    )
                )

                if scholarship_in_group and student_in_group:

                    matches.append(
                        f"{student_cert.title()} belongs to the "
                        f"{group_name.upper()} certification group."
                    )

                    break

    # Remove duplicate explanations
    matches = list(dict.fromkeys(matches))

    if matches:
        return {
            "matched": True,
            "points": 1,
            "details": matches
        }

    return {
        "matched": False,
        "points": 0,
        "details": []
    }

