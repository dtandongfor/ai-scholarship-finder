from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..matching import engine
from ..ai import recommendation_explainer

def get_recommendations(db: Session, student_id: int):
    print("===== get_recommendations CALLED =====")


    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

    scholarships = crud.get_scholarships(db)

    results = engine.match_all(
    student,
    scholarships
    )

    final_results = []

    for result in results:

        scholarship = result["scholarship"]

        explanation = recommendation_explainer.generate_explanation(
        student,
        scholarship,
        result["matched_on"],
        result["explanations"]
        )

        score = result["score"]

        if score >= 90:
            match_level = "Excellent Match"

        elif score >= 75:
            match_level = "Strong Match"

        elif score >= 50:
            match_level = "Good Match"

        elif score >= 25:
            match_level = "Potential Match"

        else:
            match_level = "Low Match"

        result["match_level"] = match_level

        result["why_you_match"] = (
        explanation["why_you_match"]
        )

    result["missing_requirements"] = (
        explanation["missing_requirements"]
    )

    result["application_tip"] = (
        explanation["application_tip"]
    )

    final_results.append(result)

    print("FINAL RESULTS:")

    for result in final_results:
        print(result)

    return {
    "student": student.name,
    "matches_found": len(final_results),
    "matches": final_results
    }
