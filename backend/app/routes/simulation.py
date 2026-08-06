from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..services import simulation_service


router = APIRouter()


@router.post(
    "/students/{student_id}/simulate",
    response_model=schemas.ImprovementSimulationResponse
)
def simulate_profile(
    student_id: int,
    improvement: schemas.ImprovementSimulationRequest,
    db: Session = Depends(get_db)
):

    return simulation_service.simulate(
        db,
        student_id,
        improvement
    )