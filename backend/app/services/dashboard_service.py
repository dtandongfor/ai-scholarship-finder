from fastapi import HTTPException

from .. import crud
from . import profile_service
from . import recommendation_service


def get_dashboard(db, student_id):

    student = crud.get_student(
        db,
        student_id
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )


    analysis = profile_service.analyze_student(
        db,
        student_id
    )


    recommendations = recommendation_service.get_recommendations(
        db,
        student_id
    )


    return {
        "student": student.name,

        "profile_strength": analysis["profile_strength"],

        "strengths": analysis["strengths"],

        "weaknesses": analysis["weaknesses"],

        "recommendations": analysis["recommendations"],

        "top_matches": recommendations["matches"],

        "improvement_plan": analysis["improvement_plan"]
    }