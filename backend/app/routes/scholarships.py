from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud
from ..services import search_service


router = APIRouter()


# ============================
# SEARCH SCHOLARSHIPS
# ============================

@router.get(
    "/search",
    response_model=list[schemas.Scholarship]
)
def search_scholarships(
    keyword: str | None = None,
    major: str | None = None,
    state: str | None = None,
    citizenship: str | None = None,
    db: Session = Depends(get_db)
):

    return search_service.search_scholarships(
        db,
        keyword,
        major,
        state,
        citizenship
    )


# ============================
# GET ALL SCHOLARSHIPS
# ============================

@router.get(
    "/",
    response_model=list[schemas.Scholarship]
)
def get_scholarships(
    db: Session = Depends(get_db)
):

    return crud.get_scholarships(db)



# ============================
# CREATE SCHOLARSHIP
# ============================

@router.post(
    "/",
    response_model=schemas.Scholarship
)
def create_scholarship(
    scholarship: schemas.ScholarshipCreate,
    db: Session = Depends(get_db)
):

    return crud.create_scholarship(
        db,
        scholarship
    )



# ============================
# GET SINGLE SCHOLARSHIP
# ============================

@router.get(
    "/{scholarship_id}",
    response_model=schemas.Scholarship
)
def get_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db)
):

    scholarship = crud.get_scholarship(
        db,
        scholarship_id
    )


    if scholarship is None:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )


    return scholarship



# ============================
# UPDATE SCHOLARSHIP
# ============================

@router.put(
    "/{scholarship_id}",
    response_model=schemas.Scholarship
)
def update_scholarship(
    scholarship_id: int,
    scholarship_update: schemas.ScholarshipUpdate,
    db: Session = Depends(get_db)
):

    scholarship = crud.update_scholarship(
        db,
        scholarship_id,
        scholarship_update
    )


    if scholarship is None:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )


    return scholarship



# ============================
# DELETE SCHOLARSHIP
# ============================

@router.delete(
    "/{scholarship_id}",
    response_model=schemas.Scholarship
)
def delete_scholarship(
    scholarship_id: int,
    db: Session = Depends(get_db)
):

    scholarship = crud.delete_scholarship(
        db,
        scholarship_id
    )


    if scholarship is None:
        raise HTTPException(
            status_code=404,
            detail="Scholarship not found"
        )


    return scholarship