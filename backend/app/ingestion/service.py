from datetime import datetime, timezone

from sqlalchemy.orm import Session

from .. import models
from .deduplication import find_existing_scholarship
from .normalizer import normalize_scholarship_data


def ingest_scholarship(db: Session, scholarship_input):
    """Create a scholarship or refresh its existing source record."""

    data = normalize_scholarship_data(
        scholarship_input.model_dump()
    )
    data["last_verified_at"] = (
        data.get("last_verified_at")
        or datetime.now(timezone.utc)
    )

    existing = find_existing_scholarship(db, data)

    if existing:
        for field, value in data.items():
            if value is not None:
                setattr(existing, field, value)

        db.commit()
        db.refresh(existing)

        return "updated", existing

    scholarship = models.Scholarship(**data)
    db.add(scholarship)
    db.commit()
    db.refresh(scholarship)

    return "created", scholarship
