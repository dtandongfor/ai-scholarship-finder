from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..services import recommendation_service


router = APIRouter()


@router.get(
    "/{student_id}",
    response_model=schemas.RecommendationResponse
)
def get_recommendations(
    student_id: int,
    db: Session = Depends(get_db)
):
    return recommendation_service.get_recommendations(
        db,
        student_id
    )