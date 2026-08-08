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

    # Highest match first
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


def match_one(student, scholarship):

    raw_score = 0
    matched_on = []
    explanations = []

    weights = scholarship.weights or {}

    # ==========================================
    # CHECK EVERY MATCHING CATEGORY
    # ==========================================

    for name, matcher in MATCHERS.items():

        check = matcher(
            student,
            scholarship
        )

        # Get the weight assigned to this category
        weight = weights.get(
            name,
            DEFAULT_WEIGHTS.get(name, 0)
        )

        if check["matched"]:

            # The scholarship weight IS the points earned.
            raw_score += weight

            matched_on.append(
                name.title()
            )

            explanations.append({
                "category": name.title(),
                "points": weight,
                "details": check.get(
                    "details",
                    []
                )
            })

    # ==========================================
    # CALCULATE MAXIMUM POSSIBLE SCORE
    # ==========================================

    max_score = 0

    for name in MATCHERS:

        weight = weights.get(
            name,
            DEFAULT_WEIGHTS.get(name, 0)
        )

        max_score += weight

    # ==========================================
    # CONVERT TO PERCENTAGE
    # ==========================================

    if max_score > 0:

        score = round(
            (raw_score / max_score) * 100
        )

    else:

        score = 0

    # ==========================================
    # DETERMINE MATCH LEVEL
    # ==========================================

    if score >= 80:

        match_level = "Excellent Match"

    elif score >= 60:

        match_level = "Strong Match"

    elif score >= 40:

        match_level = "Good Match"

    elif score >= 20:

        match_level = "Potential Match"

    else:

        match_level = "Low Match"

    # ==========================================
    # GENERATE EXPLANATION
    # ==========================================

    summary = generate_explanation({
        "scholarship": scholarship,
        "explanations": explanations
    })

    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {
        "score": score,
        "raw_score": raw_score,
        "match_level": match_level,
        "matched_on": matched_on,
        "explanations": explanations,
        "summary": summary,
        "scholarship": scholarship
    }