import os


def get_openai_api_key():
    """Read the API key at runtime so it is never stored in source code."""

    return os.getenv("OPENAI_API_KEY")


def get_openai_model():
    """Allow the deployed environment to choose the parsing model."""

    return os.getenv("OPENAI_MODEL", "gpt-5-mini")
