# Intellible early-launch checklist

## Before each catalog release

1. Run `python scripts/audit_official_links.py` from `backend`.
2. Correct every failed link. Manually review sites that block automated checks.
3. Run `python scripts/import_reviewed_scholarships.py`.
4. Run `python scripts/sync_catalog.py` first as a dry run; use `--apply` only for confirmed legacy rows with no source ID.

## Before public deployment

1. Set `INTELLIBLE_ALLOWED_ORIGINS` to the production frontend domain; do not leave a wildcard origin.
2. Use a managed production database and an external, shared rate limiter before operating multiple API instances.
3. Publish a reviewed privacy policy and terms with a support contact.
4. Test the profile-deletion flow and confirm a deleted profile cannot be retrieved.
