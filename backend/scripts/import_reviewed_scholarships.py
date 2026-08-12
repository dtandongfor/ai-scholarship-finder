"""Import reviewed scholarship records from the version-controlled seed file."""

import json
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal, migrate_schema
from app.ingestion.service import ingest_scholarship
from app.schemas import ScholarshipIngestRequest
from audit_official_links import validate_link_intents


SEED_FILE = BACKEND_DIR / "data" / "reviewed_scholarships.json"
OVERRIDES_FILE = BACKEND_DIR / "data" / "scholarship_requirement_overrides.json"


def main() -> None:
    migrate_schema()
    records = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
    link_intent_errors = validate_link_intents(records, overrides)
    if link_intent_errors:
        raise ValueError("Invalid scholarship link labels: " + "; ".join(link_intent_errors))
    created = updated = 0

    with SessionLocal() as db:
        for record in records:
            record = {
                **record,
                **overrides.get(record.get("source_id"), {}),
            }
            action, scholarship = ingest_scholarship(
                db, ScholarshipIngestRequest.model_validate(record)
            )
            if action == "created":
                created += 1
            else:
                updated += 1
            label = f"{action}: {scholarship.name}"
            print(label.encode("ascii", "backslashreplace").decode("ascii"))

    print(f"Imported {len(records)} records ({created} created, {updated} updated).")


if __name__ == "__main__":
    main()
