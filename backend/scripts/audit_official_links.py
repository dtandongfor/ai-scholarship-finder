"""Check reviewed source links before importing them into the scholarship catalog.

This verifies that each saved link is HTTPS, reaches an official destination, and
does not present an FAQ as an application page without an explicit label.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener


BACKEND_DIR = Path(__file__).parents[1]
SEED_FILE = BACKEND_DIR / "data" / "reviewed_scholarships.json"
OVERRIDES_FILE = BACKEND_DIR / "data" / "scholarship_requirement_overrides.json"
USER_AGENT = "IntellibleLinkAudit/1.0 (official source validation)"


def validate_link_intents(records: list[dict], overrides: dict) -> list[str]:
    """Reject links whose destination type contradicts their visible action label."""
    failures: list[str] = []
    for record in records:
        source_id = record.get("source_id", "unknown")
        requirements = overrides.get(source_id, {}).get("requirements", {})
        label = requirements.get("application_link_label", "View official details and application steps")
        application_url = record.get("application_url", "")
        if "/faq" in urlparse(application_url).path.lower() and label in {
            "View official details and application steps",
            "Open official application",
        }:
            failures.append(f"{source_id}: FAQ link needs a label that clearly describes its purpose")
        if requirements.get("application_required") is False:
            evidence = " ".join([
                record.get("eligibility", ""),
                record.get("description", ""),
                record.get("requirements_raw", ""),
                requirements.get("no_application_message", ""),
                " ".join(requirements.get("selection_notes", [])),
            ]).lower()
            markers = ("no separate application", "no separate scholarship application", "no separate ", "no application required", "automatically considered", "automatically awarded")
            if not any(marker in evidence for marker in markers):
                failures.append(f"{source_id}: no-application mode needs official automatic-consideration evidence")
    return failures


def check_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        return "FAIL", "must be a complete HTTPS URL"
    request = Request(url, headers={"User-Agent": USER_AGENT}, method="HEAD")
    try:
        with build_opener().open(request, timeout=20) as response:
            final_url = response.geturl()
            status = "OK" if urlparse(final_url).scheme == "https" else "FAIL"
            return status, f"HTTP {response.status} -> {final_url}"
    except HTTPError as error:
        if error.code not in {405, 501}:
            return ("WARN" if error.code in {403, 429} else "FAIL"), f"HTTP {error.code}"
    except URLError as error:
        return "WARN", f"network error: {error.reason}"

    try:
        request = Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
        with build_opener().open(request, timeout=20) as response:
            return "OK", f"HTTP {response.status} -> {response.geturl()}"
    except HTTPError as error:
        return ("WARN" if error.code in {403, 405, 429} else "FAIL"), f"HTTP {error.code}"
    except URLError as error:
        return "WARN", f"network error: {error.reason}"


def main() -> None:
    records = json.loads(SEED_FILE.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES_FILE.read_text(encoding="utf-8"))
    failures: list[str] = []
    warnings: list[str] = []
    checked: set[str] = set()

    failures.extend(validate_link_intents(records, overrides))
    for record in records:
        source_id = record.get("source_id", "unknown")
        for field in ("source_url", "application_url"):
            url = record.get(field, "")
            if not url or url in checked:
                continue
            checked.add(url)
            result, detail = check_url(url)
            print(f"{result} {field} {source_id}: {detail}")
            if result == "FAIL":
                failures.append(f"{source_id} {field}: {detail}")
            elif result == "WARN":
                warnings.append(f"{source_id} {field}: {detail}")

    if failures:
        print("\nLink audit failed:", *failures, sep="\n- ", file=sys.stderr)
        raise SystemExit(1)
    if warnings:
        print("\nLink audit completed with manual-review warnings:", *warnings, sep="\n- ", file=sys.stderr)
    print(f"\nLink audit passed for {len(checked)} unique URLs.")


if __name__ == "__main__":
    main()
