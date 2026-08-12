"""Preview or remove legacy scholarship rows not represented by the seed catalog."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models import Scholarship


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Remove only rows with no source ID.")
    args = parser.parse_args()
    source_ids = {
        item["source_id"]
        for item in json.loads((BACKEND_DIR / "data" / "reviewed_scholarships.json").read_text(encoding="utf-8"))
    }
    with SessionLocal() as db:
        legacy = db.query(Scholarship).filter(Scholarship.source_id.is_(None)).all()
        unknown = db.query(Scholarship).filter(
            Scholarship.source_id.is_not(None), ~Scholarship.source_id.in_(source_ids)
        ).all()
        print(f"Legacy rows without a source ID: {[(item.id, item.name) for item in legacy]}")
        print(f"Reviewed rows absent from the seed file: {[(item.id, item.source_id) for item in unknown]}")
        if args.apply and legacy:
            for item in legacy:
                db.delete(item)
            db.commit()
            print(f"Removed {len(legacy)} legacy rows without source IDs.")
        elif not args.apply:
            print("Dry run only. Re-run with --apply to remove the listed legacy rows.")


if __name__ == "__main__":
    main()
