from .matchers import MATCHERS
from ..config.defaults import DEFAULT_WEIGHTS
from ..ai.explanation import generate_explanation


def match_all(student, scholarships):

    results = []

    for scholarship in scholarships:

        result = match_one(
            student,
            scholarship
        )

        results.append(result)

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


def match_one(student, scholarship):

    score = 0
    matched_on = []
    explanations = []

    weights = scholarship.weights or {}

    # Calculate score
    for name, matcher in MATCHERS.items():

        check = matcher(
            student,
            scholarship
        )

        if check["matched"]:

            base_points = check["points"]

            weight = weights.get(
                name,
                DEFAULT_WEIGHTS.get(name, 1)
            )

            final_points = base_points * weight

            score += final_points

            matched_on.append(
                name.title()
            )

            explanations.append({
                "category": name.title(),
                "points": final_points,
                "details": check.get(
                    "details",
                    []
                )
            })

    # Calculate maximum possible score
    max_score = 0

    for name, matcher in MATCHERS.items():

        weight = weights.get(
            name,
            DEFAULT_WEIGHTS.get(name, 1)
        )

        try:
            base_points = matcher(
                student,
                scholarship
            )["points"]

            max_score += (
                base_points * weight
            )

        except Exception:
            pass

    # Convert to percentage
    if max_score > 0:
        percentage = round(
            (score / max_score) * 100
        )
    else:
        percentage = 0

    # Generate AI explanation
    summary = generate_explanation({
        "scholarship": scholarship,
        "explanations": explanations
    })

    return {
        "score": percentage,
        "raw_score": score,
        "matched_on": matched_on,
        "explanations": explanations,
        "summary": summary,
        "scholarship": scholarship
    }