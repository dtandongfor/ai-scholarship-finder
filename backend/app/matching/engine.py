from .matchers import MATCHERS
from ..config.defaults import DEFAULT_WEIGHTS
from ..ai.explanation import generate_explanation
from .utils import is_valid_value
from .eligibility import check_eligibility


REQUIREMENT_FIELDS = {
    "gpa": "gpa_requirement",
}


def has_requirement(scholarship, category):
    """Return whether this category has a real scholarship requirement."""

    field_name = REQUIREMENT_FIELDS.get(category, category)

    return is_valid_value(
        getattr(scholarship, field_name, None)
    )


def match_all(student, scholarships):

    results = []

    for scholarship in scholarships:

        result = match_one(
            student,
            scholarship
        )

        results.append(result)

    # Eligible scholarships appear first, then highest score first.
    results.sort(
        key=lambda x: (
            x["eligible"],
            x["score"]
        ),
        reverse=True
    )

    return results


def match_one(student, scholarship):

    raw_score = 0
    max_score = 0
    matched_on = []
    explanations = []

    weights = scholarship.weights or {}

    # Check whether the student can actually apply.
    eligibility = check_eligibility(
        student,
        scholarship
    )

    # Check every matching category.
    for name, matcher in MATCHERS.items():

        check = matcher(
            student,
            scholarship
        )

        # Use a custom scholarship weight when one exists.
        weight = weights.get(
            name,
            DEFAULT_WEIGHTS.get(name, 0)
        )

        # A list-based category can return a partial match,
        # such as 0.5 for matching half of the requirements.
        match_ratio = check.get(
            "match_ratio",
            1 if check["matched"] else 0
        )

        # Only include categories the scholarship actually requires.
        requirement_applies = has_requirement(
            scholarship,
            name
        )

        if requirement_applies:
            max_score += weight

        # A blank scholarship field earns no points.
        earned_points = (
            weight * match_ratio
            if requirement_applies
            else 0
        )

        if earned_points > 0:

            raw_score += earned_points

            matched_on.append(
                name.title()
            )

            explanations.append({
                "category": name.title(),
                "points": round(earned_points, 2),
                "details": check.get(
                    "details",
                    []
                )
            })

    # Convert the weighted points to a percentage.
    if max_score > 0:

        score = round(
            (raw_score / max_score) * 100
        )

    else:

        score = 0

    # Determine the user-facing match label.
    if not eligibility["eligible"]:

        match_level = "Not Eligible"

    elif score >= 80:

        match_level = "Excellent Match"

    elif score >= 60:

        match_level = "Strong Match"

    elif score >= 40:

        match_level = "Good Match"

    elif score >= 20:

        match_level = "Potential Match"

    else:

        match_level = "Low Match"

    # Generate the explanation shown to the student.
    summary = generate_explanation({
        "scholarship": scholarship,
        "explanations": explanations
    })

    return {
        "score": score,
        "raw_score": round(raw_score, 2),
        "eligible": eligibility["eligible"],
        "ineligibility_reasons": (
            eligibility["ineligibility_reasons"]
        ),
        "match_level": match_level,
        "matched_on": matched_on,
        "explanations": explanations,
        "summary": summary,
        "scholarship": scholarship
    }