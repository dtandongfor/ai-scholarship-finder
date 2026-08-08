from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models


def find_existing_scholarship(db: Session, data: dict):
    """Find the same scholarship using the most trustworthy identifiers first."""

    source_name = data.get("source_name")
    source_id = data.get("source_id")

    if source_name and source_id:
        existing = db.query(models.Scholarship).filter(
            func.lower(models.Scholarship.source_name)
            == source_name.lower(),
            models.Scholarship.source_id == source_id,
        ).first()

        if existing:
            return existing

    for url_field in ("source_url", "application_url"):
        url = data.get(url_field)

        if url:
            existing = db.query(models.Scholarship).filter(
                getattr(models.Scholarship, url_field) == url
            ).first()

            if existing:
                return existing

    # A final fallback helps when the source provides no stable ID or URL.
    if data.get("name") and data.get("provider"):
        return db.query(models.Scholarship).filter(
            func.lower(models.Scholarship.name) == data["name"].lower(),
            func.lower(models.Scholarship.provider)
            == data["provider"].lower(),
        ).first()

    return None
