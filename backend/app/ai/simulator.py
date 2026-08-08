from copy import deepcopy

from ..matching.engine import match_one


def simulate_improvement(student, scholarships, improvement):

    current_matches = 0
    projected_matches = 0

    current_scores = []
    projected_scores = []


    # Check current profile
    for scholarship in scholarships:

        result = match_one(
            student,
            scholarship
        )

        current_scores.append(
            result["score"]
        )

        if result["eligible"] and result["score"] >= 50:
            current_matches += 1


    # Copy student so database is not changed
    simulated_student = deepcopy(student)


    category = improvement.category
    value = improvement.value


    # Apply improvement
    setattr(
        simulated_student,
        category,
        value
    )


    # Check improved profile
    for scholarship in scholarships:

        result = match_one(
            simulated_student,
            scholarship
        )

        projected_scores.append(
            result["score"]
        )

        if result["eligible"] and result["score"] >= 50:
            projected_matches += 1


    current_average = round(
        sum(current_scores) / len(current_scores)
    ) if current_scores else 0


    projected_average = round(
        sum(projected_scores) / len(projected_scores)
    ) if projected_scores else 0


    score_change = (
        projected_average -
        current_average
    )


    return {
        "improvement": category,
        "current_matches": current_matches,
        "projected_matches": projected_matches,
        "increase": projected_matches - current_matches,

        "current_average_score": current_average,
        "projected_average_score": projected_average,
        "score_change": score_change,

        "impact": (
            f"Adding {category} changed your "
            f"profile score by {score_change} points."
        )
    }
