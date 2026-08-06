from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas, crud


router = APIRouter()


@router.get("/", response_model=list[schemas.Scholarship])
def get_scholarships(db: Session = Depends(get_db)):
    return crud.get_scholarships(db)

@router.get("/{scholarship_id}", response_model=schemas.Scholarship)
def get_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    scholarship = db.query(models.Scholarship).filter(
        models.Scholarship.id == scholarship_id
    ).first()

    if scholarship is None:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    return scholarship

@router.put("/{scholarship_id}", response_model=schemas.Scholarship)
def update_scholarship(
    scholarship_id: int,
    updated: schemas.ScholarshipUpdate,
    db: Session = Depends(get_db)
):
    scholarship = (
        db.query(models.Scholarship)
        .filter(models.Scholarship.id == scholarship_id)
        .first()
    )

    if scholarship is None:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    scholarship.name = updated.name
    scholarship.provider = updated.provider
    scholarship.amount = updated.amount
    scholarship.deadline = updated.deadline
    scholarship.major = updated.major
    scholarship.gpa_requirement = updated.gpa_requirement
    scholarship.eligibility = updated.eligibility

    db.commit()
    db.refresh(scholarship)

    return scholarship

@router.delete("/{scholarship_id}")
def delete_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    scholarship = (
        db.query(models.Scholarship)
        .filter(models.Scholarship.id == scholarship_id)
        .first()
    )

    if scholarship is None:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )

    db.delete(scholarship)
    db.commit()

    return {"message": "Scholarship deleted successfully"}

@router.post("/", response_model=schemas.Scholarship)
def create_scholarship(
    scholarship: schemas.ScholarshipCreate,
    db: Session = Depends(get_db)
):
    return crud.create_scholarship(db, scholarship)