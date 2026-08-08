import json

from openai import APIConnectionError, APIStatusError, RateLimitError

from ..config.settings import get_openai_api_key, get_openai_model
from ..schemas import ScholarshipParsedData


class ScholarshipParserError(Exception):
    """Raised when a scholarship description cannot be parsed safely."""


class AIConfigurationError(ScholarshipParserError):
    """Raised when the OpenAI dependency or API key is unavailable."""


class AIUsageLimitError(ScholarshipParserError):
    """Raised when the OpenAI account has no remaining API quota."""


class AIServiceError(ScholarshipParserError):
    """Raised when the OpenAI service cannot complete a request."""


PARSER_INSTRUCTIONS = """
You extract scholarship information from a source description.
Return only information that is explicitly stated in the source text.
Do not infer eligibility, dates, amounts, or requirements.
Use null when a field is not stated. Keep comma-separated lists concise.
For skills, majors, interests, certifications, and activities, return only
the normalized value (for example, "Python" rather than
"Python experience preferred"). Keep GPA, state, and citizenship in their
own fields instead of repeating them in eligibility.
""".strip()


PARSED_SCHOLARSHIP_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": ["string", "null"]},
        "provider": {"type": ["string", "null"]},
        "amount": {"type": ["string", "null"]},
        "deadline": {"type": ["string", "null"]},
        "major": {"type": ["string", "null"]},
        "gpa_requirement": {"type": ["string", "null"]},
        "eligibility": {"type": ["string", "null"]},
        "state": {"type": ["string", "null"]},
        "citizenship": {"type": ["string", "null"]},
        "interests": {"type": ["string", "null"]},
        "skills": {"type": ["string", "null"]},
        "projects": {"type": ["string", "null"]},
        "leadership": {"type": ["string", "null"]},
        "volunteer": {"type": ["string", "null"]},
        "certifications": {"type": ["string", "null"]},
        "requirements_raw": {"type": ["string", "null"]},
    },
    "required": [
        "name", "provider", "amount", "deadline", "major",
        "gpa_requirement", "eligibility", "state", "citizenship",
        "interests", "skills", "projects", "leadership", "volunteer",
        "certifications", "requirements_raw",
    ],
    "additionalProperties": False,
}


def _create_client():
    api_key = get_openai_api_key()

    if not api_key:
        raise AIConfigurationError(
            "OPENAI_API_KEY is not configured."
        )

    try:
        from openai import OpenAI
    except ImportError as error:
        raise AIConfigurationError(
            "The openai package is not installed."
        ) from error

    return OpenAI(api_key=api_key)


def parse_scholarship_description(
    description: str,
    client=None,
    model: str | None = None,
):
    """Use structured AI output to turn source text into a scholarship draft."""

    if not description or not description.strip():
        raise ScholarshipParserError(
            "A scholarship description is required."
        )

    client = client or _create_client()

    try:
        response = client.responses.create(
            model=model or get_openai_model(),
            instructions=PARSER_INSTRUCTIONS,
            input=description,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "scholarship_extraction",
                    "strict": True,
                    "schema": PARSED_SCHOLARSHIP_SCHEMA,
                }
            },
        )
        parsed_data = json.loads(response.output_text)
        return ScholarshipParsedData.model_validate(parsed_data)
    except ScholarshipParserError:
        raise
    except RateLimitError as error:
        raise AIUsageLimitError(
            "OpenAI API credits are unavailable. Add credits and try again."
        ) from error
    except (APIConnectionError, APIStatusError) as error:
        raise AIServiceError(
            "The OpenAI service could not process this request. Try again later."
        ) from error
    except (json.JSONDecodeError, ValueError, TypeError) as error:
        raise ScholarshipParserError(
            "The AI response was not a valid scholarship record."
        ) from error
