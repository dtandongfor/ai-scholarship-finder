"""Seed a brand-new database with the reviewed, version-controlled catalog."""

import json
from pathlib import Path

from . import models
from .database import SessionLocal
from .ingestion.service import ingest_scholarship
from .schemas import ScholarshipIngestRequest

BACKEND_DIR = Path(__file__).parents[1]
SEED_FILE = BACKEND_DIR / "data" / "reviewed_scholarships.json"
OVERRIDES_FILE = BACKEND_DIR / "data" / "scholarship_requirement_overrides.json"


def seed_reviewed_catalog_if_empty() -> int:
    """Load reviewed records only when a newly connected database has none."""

    with SessionLocal() as db:
        if db.query(models.Scholarship.id).first() is not None:
            return 0

        records = json.loads(SEED_FILE.read_text(encoding="utf-8"))
        overrides = json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
        for record in records:
            merged_record = {**record, **overrides.get(record.get("source_id"), {})}
            ingest_scholarship(db, ScholarshipIngestRequest.model_validate(merged_record))
        return len(records)
