from fastapi import APIRouter, HTTPException

from .. import schemas
from ..ai.scholarship_parser import (
    AIConfigurationError,
    AIServiceError,
    AIUsageLimitError,
    ScholarshipParserError,
    parse_scholarship_description,
)


router = APIRouter()


@router.post(
    "/scholarships/parse",
    response_model=schemas.ScholarshipParseResponse,
)
def parse_scholarship(
    source: schemas.ScholarshipParseRequest,
):
    """Create a reviewable scholarship draft from raw source text."""

    try:
        parsed = parse_scholarship_description(source.description)
    except AIConfigurationError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except AIUsageLimitError as error:
        raise HTTPException(status_code=429, detail=str(error)) from error
    except AIServiceError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except ScholarshipParserError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    missing_required_fields = [
        field
        for field in ("name", "provider")
        if not getattr(parsed, field)
    ]

    return {
        "parsed": parsed,
        "source_name": source.source_name,
        "source_id": source.source_id,
        "source_url": source.source_url,
        "application_url": source.application_url,
        "description": source.description,
        "ready_to_ingest": not missing_required_fields,
        "missing_required_fields": missing_required_fields,
    }
