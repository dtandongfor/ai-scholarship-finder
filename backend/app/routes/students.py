from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, crud
from ..services import profile_service
from ..services import resume_service

router = APIRouter()


@router.post("/resume-preview", response_model=schemas.ResumePrefillResponse)
async def preview_resume(resume: UploadFile = File(...)):
    """Extract editable profile suggestions without persisting the resume."""
    suggestions, review_notes = await resume_service.parse_resume_upload(resume)
    return {"suggestions": suggestions, "review_notes": review_notes}

@router.get("/", response_model=list[schemas.Student])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@router.post("/", response_model=schemas.Student)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_student(db, student)

@router.get("/{student_id}", response_model=schemas.Student)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@router.put("/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    student = crud.update_student(
        db,
        student_id,
        student_update
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@router.delete("/{student_id}", response_model=schemas.Student)
def delete_student(
    student_id: int,
    confirmation: schemas.StudentDeletionRequest,
    db: Session = Depends(get_db)
):
    student = crud.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if (student.email or "").strip().lower() != confirmation.email.strip().lower():
        raise HTTPException(status_code=403, detail="Enter the email on this profile to confirm deletion.")
    student = crud.delete_student(db, student_id)
    return student

@router.get(
    "/{student_id}/analysis",
    response_model=schemas.ProfileAnalysisResponse
)
def analyze_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    return profile_service.analyze_student(
        db,
        student_id
    )
