from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..services import dashboard_service


router = APIRouter()


@router.get(
    "/{student_id}",
    response_model=schemas.DashboardResponse
)
def get_dashboard(
    student_id: int,
    db: Session = Depends(get_db)
):

    return dashboard_service.get_dashboard(
        db,
        student_id
    )