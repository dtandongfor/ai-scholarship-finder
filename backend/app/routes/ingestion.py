from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..ingestion import service


router = APIRouter()


@router.post(
    "/scholarships",
    response_model=schemas.ScholarshipIngestResponse,
)
def ingest_scholarship(
    scholarship: schemas.ScholarshipIngestRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    """Import a scholarship from a trusted source or a future AI parser."""

    action, saved_scholarship = service.ingest_scholarship(
        db,
        scholarship,
    )

    if action == "created":
        response.status_code = status.HTTP_201_CREATED

    return {
        "action": action,
        "scholarship": saved_scholarship,
    }
