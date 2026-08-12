import re

from .utils import is_valid_value
from .verified_requirements import evaluate_verified_requirements


STATE_ABBREVIATIONS = {
    "alabama": "al",
    "alaska": "ak",
    "arizona": "az",
    "arkansas": "ar",
    "california": "ca",
    "colorado": "co",
    "connecticut": "ct",
    "delaware": "de",
    "florida": "fl",
    "georgia": "ga",
    "hawaii": "hi",
    "idaho": "id",
    "illinois": "il",
    "indiana": "in",
    "iowa": "ia",
    "kansas": "ks",
    "kentucky": "ky",
    "louisiana": "la",
    "maine": "me",
    "maryland": "md",
    "massachusetts": "ma",
    "michigan": "mi",
    "minnesota": "mn",
    "mississippi": "ms",
    "missouri": "mo",
    "montana": "mt",
    "nebraska": "ne",
    "nevada": "nv",
    "new hampshire": "nh",
    "new jersey": "nj",
    "new mexico": "nm",
    "new york": "ny",
    "north carolina": "nc",
    "north dakota": "nd",
    "ohio": "oh",
    "oklahoma": "ok",
    "oregon": "or",
    "pennsylvania": "pa",
    "rhode island": "ri",
    "south carolina": "sc",
    "south dakota": "sd",
    "tennessee": "tn",
    "texas": "tx",
    "utah": "ut",
    "vermont": "vt",
    "virginia": "va",
    "washington": "wa",
    "west virginia": "wv",
    "wisconsin": "wi",
    "wyoming": "wy",
}


def normalize_state(value):
    """Compare state names and postal abbreviations consistently."""

    normalized = str(value).strip().lower()
    return STATE_ABBREVIATIONS.get(normalized, normalized)


def citizenship_matches(student_value, required_value):
    """Handle the common ``US`` profile value and source wording safely."""

    student = str(student_value).strip().lower()
    required = str(required_value).strip().lower()

    if student in {"us", "u.s.", "us citizen", "u.s. citizen"}:
        return "u.s. citizen" in required or "us citizen" in required

    if student in {"permanent resident", "legal permanent resident"}:
        return "permanent resident" in required

    return student == required


def parse_gpa(value):
    match = re.search(r"\d(?:\.\d+)?", str(value))
    return float(match.group()) if match else None


def check_eligibility(student, scholarship):
    """
    Checks rules that determine whether the student can apply.

    Returns an eligibility status and clear reasons if the student
    does not meet a required rule.
    """

    reasons = []

    # Student type is optional on profiles, but decisive when both the
    # scholarship and the student's status are known.
    if is_valid_value(getattr(scholarship, "eligible_student_types", None)):
        student_type = getattr(student, "student_type", None)
        if student_type and student_type not in {
            item.strip().lower()
            for item in scholarship.eligible_student_types.split(",")
        }:
            reasons.append(
                "This opportunity is not available for your student type."
            )

    # A missing income never excludes a student; it simply means we cannot
    # verify an income-based opportunity yet.
    max_income = getattr(scholarship, "max_household_income", None)
    household_income = getattr(student, "household_income", None)
    if max_income is not None and household_income is not None:
        if household_income > max_income:
            reasons.append(
                f"Available to households with income up to ${max_income:,}."
            )

    min_sat = getattr(scholarship, "min_sat_score", None)
    min_act = getattr(scholarship, "min_act_score", None)
    if min_sat is not None or min_act is not None:
        sat_score = getattr(student, "sat_score", None)
        act_score = getattr(student, "act_score", None)
        meets_sat = min_sat is not None and sat_score is not None and sat_score >= min_sat
        meets_act = min_act is not None and act_score is not None and act_score >= min_act
        if (sat_score is not None or act_score is not None) and not (meets_sat or meets_act):
            reasons.append("Your available test score does not meet this opportunity's minimum.")

    # GPA is a minimum requirement.
    if is_valid_value(scholarship.gpa_requirement):
        try:
            student_gpa = parse_gpa(student.gpa)
            required_gpa = parse_gpa(scholarship.gpa_requirement)
            if student_gpa is None or required_gpa is None:
                raise ValueError

            if student_gpa < required_gpa:
                reasons.append(
                    f"Requires a minimum GPA of {required_gpa:.2f}; "
                    f"your GPA is {student_gpa:.2f}."
                )
        except (TypeError, ValueError):
            reasons.append("The GPA requirement could not be checked.")

    # Citizenship must match when the scholarship specifies one.
    if is_valid_value(scholarship.citizenship):
        if not citizenship_matches(
            student.citizenship,
            scholarship.citizenship,
        ):
            reasons.append(
                f"Requires {scholarship.citizenship} citizenship."
            )

    # State must match when the scholarship is location-specific.
    if is_valid_value(scholarship.state):
        student_state = normalize_state(student.state)
        required_state = normalize_state(scholarship.state)

        if student_state != required_state:
            reasons.append(
                f"Available only to students in {scholarship.state}."
            )

    verified = evaluate_verified_requirements(student, scholarship)
    reasons.extend(verified["disqualifiers"])

    return {
        "eligible": not reasons,
        "ineligibility_reasons": reasons,
        "review_items": verified["review_items"],
        "application_checklist": verified["application_checklist"],
        "selection_notes": verified["selection_notes"],
    }
