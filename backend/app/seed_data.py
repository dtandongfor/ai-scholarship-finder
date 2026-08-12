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


def sync_reviewed_catalog() -> tuple[int, int]:
    """Upsert the reviewed catalog so deployment updates reach the live database."""

    with SessionLocal() as db:
        records = json.loads(SEED_FILE.read_text(encoding="utf-8"))
        overrides = json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
        created = updated = 0
        for record in records:
            merged_record = {**record, **overrides.get(record.get("source_id"), {})}
            action, _ = ingest_scholarship(db, ScholarshipIngestRequest.model_validate(merged_record))
            if action == "created":
                created += 1
            else:
                updated += 1
        return created, updated
