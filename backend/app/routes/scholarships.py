from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas


router = APIRouter()


@router.get("/", response_model=list[schemas.Scholarship])
def get_scholarships(db: Session = Depends(get_db)):
    scholarships = db.query(models.Scholarship).all()
    return scholarships

@router.get("/{scholarship_id}", response_model=schemas.Scholarship)
def get_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db)
):
    scholarship = db.query(models.Scholarship).filter(
        models.Scholarship.id == scholarship_id
    ).first()

    return scholarship

@router.post("/", response_model=schemas.Scholarship)
def create_scholarship(
    scholarship: schemas.ScholarshipCreate,
    db: Session = Depends(get_db)
):
    db_scholarship = models.Scholarship(
        name=scholarship.name,
        provider=scholarship.provider,
        amount=scholarship.amount,
        deadline=scholarship.deadline,
        major=scholarship.major,
        gpa_requirement=scholarship.gpa_requirement,
        eligibility=scholarship.eligibility
    )

    db.add(db_scholarship)
    db.commit()
    db.refresh(db_scholarship)

    return db_scholarship