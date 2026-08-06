from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..matching import engine


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

    print("FINAL RESULTS:")
    for r in results:
        print(r)

    return {
        "student": student.name,
        "matches_found": len(results),
        "matches": results
    }