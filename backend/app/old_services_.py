print("LOADED MY SERVICES.PY")

from fastapi import HTTPException
from . import crud


def get_recommendations(db, student_id: int):
    print("===== get_recommendations CALLED =====")

    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    scholarships = crud.get_scholarships(db)

    results = []

    for scholarship in scholarships:

        score = 0
        matched_on = []

        # Major Match
        if scholarship.major:
            if scholarship.major.lower() == student.major.lower():
                score += 40
                matched_on.append("Major")
            else:
                continue

        # GPA Match
        try:
            required_gpa = float(scholarship.gpa_requirement)
            student_gpa = float(student.gpa)

            if student_gpa >= required_gpa:
                score += 30
                matched_on.append("GPA")
            else:
                continue

        except (ValueError, TypeError):
            pass

        # State Match
        if scholarship.state and student.state:
            if scholarship.state.strip().lower() == student.state.strip().lower():
                score += 10
                matched_on.append("State")

        # Citizenship Match
        if scholarship.citizenship and student.citizenship:
            if scholarship.citizenship.strip().lower() == student.citizenship.strip().lower():
                score += 10
                matched_on.append("Citizenship")

        # Interests Match
        if scholarship.interests and student.interests:

            scholarship_interests = [
                interest.strip().lower()
                for interest in scholarship.interests.split(",")
            ]

            student_interests = [
                interest.strip().lower()
                for interest in student.interests.split(",")
            ]

            if any(
                interest in scholarship_interests
                for interest in student_interests
            ):
                score += 10
                matched_on.append("Interests")

        print(
            f"{scholarship.name}: "
            f"score={score}, matched_on={matched_on}"
        )

        results.append({
            "score": score,
            "matched_on": matched_on,
            "scholarship": scholarship
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    print("FINAL RESULTS:")
    for r in results:
        print(r)

    return {
        "student": student.name,
        "matches_found": len(results),
        "matches": results
    }