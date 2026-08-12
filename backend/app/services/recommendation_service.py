from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import crud, models
from ..matching import engine
from ..matching.eligibility import normalize_state, parse_gpa
from ..matching.matchers import MATCHERS
from ..matching.utils import is_valid_value
from ..ai import recommendation_explainer


FOCUS_CATEGORIES = {
    "major",
    "interests",
    "skills",
    "projects",
    "leadership",
    "volunteer",
    "certifications",
}


def has_meaningful_match(student, scholarship, result):
    """Require an affirmative, profile-backed fit before showing a result."""

    # A known mismatch on a source-specified field is more important than a
    # generic fit such as the same student stage. For example, a first-year
    # computer-science student should not see a medicine-only opportunity.
    for category, matcher in MATCHERS.items():
        field_name = engine.REQUIREMENT_FIELDS.get(category, category)
        requirement = getattr(scholarship, field_name, None)
        profile_value = getattr(student, category, None)
        if not is_valid_value(requirement):
            continue

        matched = matcher(student, scholarship).get("matched")
        # A field-specific opportunity needs a verified alignment; merely
        # omitting interests or experience cannot be treated as a match.
        if category in FOCUS_CATEGORIES and (
            not is_valid_value(profile_value) or not matched
        ):
            return False

        if is_valid_value(profile_value) and not matched:
            return False

    if result["score"] > 0:
        return True

    eligible_types = getattr(scholarship, "eligible_student_types", None)
    if student.student_type and eligible_types and student.student_type in {
        item.strip().lower() for item in eligible_types.split(",")
    }:
        return True

    max_income = getattr(scholarship, "max_household_income", None)
    if (
        student.household_income is not None
        and max_income is not None
        and student.household_income <= max_income
    ):
        return True

    return False


def build_match_reasons(student, scholarship, result, explanation):
    """Give students concrete reasons instead of a generic match message."""

    reasons = []

    if scholarship.state and normalize_state(student.state) == normalize_state(scholarship.state):
        reasons.append(
            f"This is an in-state opportunity for {scholarship.state}, matching your home state."
        )

    if scholarship.gpa_requirement:
        student_gpa = parse_gpa(student.gpa)
        required_gpa = parse_gpa(scholarship.gpa_requirement)
        if student_gpa is not None and required_gpa is not None and student_gpa >= required_gpa:
            reasons.append(
                f"Your {student_gpa:.2f} GPA meets its {required_gpa:.2f} minimum."
            )

    student_type = getattr(student, "student_type", None)
    eligible_types = getattr(scholarship, "eligible_student_types", None)
    if student_type and eligible_types and student_type in {
        item.strip().lower() for item in eligible_types.split(",")
    }:
        label = student_type.replace("_", " ")
        reasons.append(f"It is open to {label} students.")

    income = getattr(student, "household_income", None)
    max_income = getattr(scholarship, "max_household_income", None)
    if income is not None and max_income is not None and income <= max_income:
        reasons.append(
            f"Your household income is within its published ${max_income:,} limit."
        )

    sat = getattr(student, "sat_score", None)
    min_sat = getattr(scholarship, "min_sat_score", None)
    if sat is not None and min_sat is not None and sat >= min_sat:
        reasons.append(f"Your SAT score meets its {min_sat} minimum.")

    act = getattr(student, "act_score", None)
    min_act = getattr(scholarship, "min_act_score", None)
    if act is not None and min_act is not None and act >= min_act:
        reasons.append(f"Your ACT score meets its {min_act} minimum.")

    for reason in explanation["why_you_match"]:
        if reason not in reasons:
            reasons.append(reason)

    if not reasons:
        if result["score"] == 0:
            reasons.append(
                "No profile factor could be scored for this opportunity yet. It is shown because none of its structured rules rule you out; review the official requirements before applying."
            )
        else:
            reasons.append(
                "Your profile matches one or more published requirements for this opportunity."
            )

    return reasons


def get_recommendations(db: Session, student_id: int):

    student = crud.get_student(
        db,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Students should only see opportunities that are currently active.
    scholarships = (
        db.query(models.Scholarship)
        .filter(models.Scholarship.is_active.is_(True))
        .all()
    )

    # Match the student against ALL scholarships
    results = engine.match_all(
        student,
        scholarships
    )

    final_results = []

    # Main recommendations should contain only opportunities the student can
    # currently apply for. Ineligible results remain available to internal
    # tools through the matching engine, along with their reasons.
    for result in results:

        scholarship = result["scholarship"]
        if (
            not result["eligible"]
            or not has_meaningful_match(student, scholarship, result)
            or not scholarship.requirements_complete
            or result["review_items"]
        ):
            continue

        explanation = recommendation_explainer.generate_explanation(
            student,
            scholarship,
            result["matched_on"],
            result["explanations"]
        )

        result["why_you_match"] = build_match_reasons(
            student,
            scholarship,
            result,
            explanation,
        )

        result["missing_requirements"] = (
            explanation["missing_requirements"]
        )
        # Keep source-reviewed details visible even when the profile does not
        # yet have a field for them (for example, assets, coursework, or a
        # nomination). They must not silently look like a confirmed match.
        result["unassessed_requirements"] = (
            [scholarship.requirements_raw]
            if scholarship.requirements_raw
            else []
        )

        result["application_tip"] = (
            explanation["application_tip"]
        )
        result["match_status"] = (
            "Confirmed fit"
            if scholarship.requirements_complete and not result["review_items"]
            else "Needs review"
        )

        # IMPORTANT:
        # Append each scholarship INSIDE the loop
        final_results.append(result)

    return {
        "student": student.name,
        "matches_found": len(final_results),
        "matches": final_results
    }
