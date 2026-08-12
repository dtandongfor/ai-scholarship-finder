from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..ingestion import service
from ..sources import list_sources


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


@router.post(
    "/scholarships/batch",
    response_model=schemas.ScholarshipBatchIngestResponse,
    status_code=status.HTTP_201_CREATED,
)
def ingest_scholarship_batch(
    batch: schemas.ScholarshipBatchIngestRequest,
    db: Session = Depends(get_db),
):
    """Save reviewed records from an approved public source in one request."""

    created = 0
    updated = 0
    saved_scholarships = []

    for scholarship in batch.scholarships:
        action, saved_scholarship = service.ingest_scholarship(db, scholarship)
        saved_scholarships.append(saved_scholarship)
        if action == "created":
            created += 1
        else:
            updated += 1

    return {
        "created": created,
        "updated": updated,
        "scholarships": saved_scholarships,
    }


@router.get("/sources", response_model=list[schemas.ScholarshipSource])
def get_scholarship_sources():
    """List public sources approved for reviewed scholarship imports."""

    return list_sources()
