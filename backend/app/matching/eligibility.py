from .utils import is_valid_value


def check_eligibility(student, scholarship):
    """
    Checks rules that determine whether the student can apply.

    Returns an eligibility status and clear reasons if the student
    does not meet a required rule.
    """

    reasons = []

    # GPA is a minimum requirement.
    if is_valid_value(scholarship.gpa_requirement):
        try:
            student_gpa = float(student.gpa)
            required_gpa = float(scholarship.gpa_requirement)

            if student_gpa < required_gpa:
                reasons.append(
                    f"Requires a minimum GPA of {required_gpa:.2f}; "
                    f"your GPA is {student_gpa:.2f}."
                )
        except (TypeError, ValueError):
            reasons.append("The GPA requirement could not be checked.")

    # Citizenship must match when the scholarship specifies one.
    if is_valid_value(scholarship.citizenship):
        student_citizenship = str(student.citizenship).strip().lower()
        required_citizenship = str(scholarship.citizenship).strip().lower()

        if student_citizenship != required_citizenship:
            reasons.append(
                f"Requires {scholarship.citizenship} citizenship."
            )

    # State must match when the scholarship is location-specific.
    if is_valid_value(scholarship.state):
        student_state = str(student.state).strip().lower()
        required_state = str(scholarship.state).strip().lower()

        if student_state != required_state:
            reasons.append(
                f"Available only to students in {scholarship.state}."
            )

    return {
        "eligible": not reasons,
        "ineligibility_reasons": reasons,
    }