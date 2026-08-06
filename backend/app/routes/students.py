from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, crud
from ..services import profile_service

router = APIRouter()

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
    db: Session = Depends(get_db)
):
    student = crud.delete_student(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

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