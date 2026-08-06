from fastapi import HTTPException

from .. import crud
from ..ai import advisor
from ..ai import improvement_planner

def analyze_student(db, student_id: int):

    student = crud.get_student(db, student_id)
    scholarships = crud.get_scholarships(db)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    score = 0

    strengths = []
    weaknesses = []
    recommendations = []

    # GPA
    try:
        gpa = float(student.gpa)

        if gpa >= 3.8:
            score += 25
            strengths.append("Excellent GPA")

        elif gpa >= 3.5:
            score += 20
            strengths.append("Strong GPA")

        elif gpa >= 3.0:
            score += 15

        else:
            weaknesses.append("Low GPA")
            recommendations.append(
                "Improve your GPA before applying."
            )

    except (TypeError, ValueError):
        weaknesses.append("No GPA provided")

    # Skills
    if student.skills:
        score += 15
        strengths.append("Strong technical skills")
    else:
        weaknesses.append("No skills listed")
        recommendations.append(
            "Add technical skills to your profile."
        )

    # Projects
    if student.projects:
        score += 15
        strengths.append("Relevant projects")
    else:
        weaknesses.append("No projects listed")
        recommendations.append(
            "Complete a portfolio project."
        )

    # Leadership
    if student.leadership:
        score += 15
        strengths.append("Leadership experience")
    else:
        weaknesses.append("No leadership experience")
        recommendations.append(
            "Join a student organization."
        )

    # Volunteer
    if student.volunteer:
        score += 10
        strengths.append("Volunteer experience")
    else:
        weaknesses.append("Limited volunteer experience")
        recommendations.append(
            "Volunteer in your community."
        )

    # Certifications
    if student.certifications:
        score += 10
        strengths.append("Industry certifications")
    else:
        weaknesses.append("No certifications")
        recommendations.append(
            "Earn an industry certification."
        )

    # Interests
    if student.interests:
        score += 10

    ai_feedback = advisor.generate_advice(
    student,
    {
        "profile_strength": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
    },
        )

    improvement_plan = improvement_planner.generate_plan(
        student,
        scholarships,
    )

    plan = improvement_plan

    return {
        "student": student.name,
        "profile_strength": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "ai_summary": ai_feedback["summary"],
        "ai_advice": ai_feedback["advice"],
        "improvement_plan": plan
    }