from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..services import search_service


router = APIRouter()


@router.get(
    "/scholarships/search",
    response_model=list[schemas.Scholarship]
)
def search(
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