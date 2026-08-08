from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_PARAMETERS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
}


def normalize_text(value):
    """Trim text and collapse repeated whitespace."""

    if value is None:
        return None

    cleaned = " ".join(str(value).split())
    return cleaned or None


def normalize_url(value):
    """Remove harmless tracking parameters so duplicate URLs compare equally."""

    if not value:
        return None

    parsed = urlsplit(str(value).strip())
    query = [
        (key, item)
        for key, item in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_")
        and key.lower() not in TRACKING_PARAMETERS
    ]

    path = parsed.path.rstrip("/") or "/"

    return urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            path,
            urlencode(query, doseq=True),
            "",
        )
    )


def normalize_scholarship_data(data):
    """Normalize fields that are used for display and duplicate detection."""

    normalized = dict(data)

    for field in (
        "name",
        "provider",
        "source_name",
        "source_id",
        "description",
        "requirements_raw",
    ):
        if field in normalized:
            normalized[field] = normalize_text(normalized[field])

    for field in ("source_url", "application_url"):
        if field in normalized:
            normalized[field] = normalize_url(normalized[field])

    return normalized
