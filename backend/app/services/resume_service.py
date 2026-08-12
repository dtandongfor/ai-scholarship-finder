"""Local, suggestion-only resume extraction for profile prefill.

The uploaded content is used only for this preview and is never stored in the
student profile or scholarship database.
"""

from __future__ import annotations

from io import BytesIO
import re

from fastapi import HTTPException, UploadFile
from docx import Document
from pypdf import PdfReader


MAX_RESUME_BYTES = 2 * 1024 * 1024
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def _extension(filename: str | None) -> str:
    name = (filename or "").lower().strip()
    return f".{name.rsplit('.', 1)[1]}" if "." in name else ""


def _extract_text(content: bytes, extension: str) -> str:
    try:
        if extension == ".txt":
            return content.decode("utf-8", errors="replace")
        if extension == ".docx":
            document = Document(BytesIO(content))
            return "\n".join(paragraph.text for paragraph in document.paragraphs)
        if extension == ".pdf":
            return "\n".join(page.extract_text() or "" for page in PdfReader(BytesIO(content)).pages)
    except Exception as exc:
        raise HTTPException(status_code=422, detail="We couldn't read that resume. Try a text-based PDF, DOCX, or TXT file.") from exc
    raise HTTPException(status_code=415, detail="Upload a PDF, DOCX, or TXT resume.")


def _section(text: str, headings: tuple[str, ...]) -> str | None:
    lines = text.splitlines()
    normalized_headings = {heading.lower() for heading in headings}
    start = next(
        (index for index, line in enumerate(lines)
         if line.strip().rstrip(":").lower() in normalized_headings),
        None,
    )
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped and re.fullmatch(r"[A-Z][A-Z &/,-]{2,}:?", stripped):
            break
        body.append(stripped)
    value = re.sub(r"\s+", " ", " ".join(body)).strip(" -\t")
    return value[:500] or None


def suggestions_from_text(text: str) -> dict[str, str]:
    """Return conservative, editable suggestions from common resume patterns."""
    compact = re.sub(r"\r", "", text)
    suggestions: dict[str, str] = {}
    email = re.search(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", compact, re.I)
    if email:
        suggestions["email"] = email.group(0)
    gpa = re.search(r"\b(?:cumulative\s+)?g\.?p\.?a\.?\s*(?:of|:)?\s*([0-4](?:\.\d{1,2})?)\b", compact, re.I)
    if gpa:
        suggestions["gpa"] = gpa.group(1)
    major = re.search(
        r"\b(?:major(?:\s+in)?|b\.?s\.?|bachelor(?:\s+of\s+science)?|b\.?a\.?|associate(?:\s+of\s+(?:science|arts))?)\s*(?:in|:)\s*([A-Za-z][A-Za-z &/.-]{2,70})",
        compact,
        re.I,
    )
    if major:
        suggestions["major"] = major.group(1).split("\n")[0].strip(" ,.-")
    school = next(
        (line.strip(" ,.-") for line in compact.splitlines()
         if re.search(r"\b(?:university|college|community college|institute)\b", line, re.I)
         and 3 <= len(line.strip()) <= 100),
        None,
    )
    if school:
        suggestions["university"] = school
    for field, headings in {
        "skills": ("skills", "technical skills", "core competencies"),
        "certifications": ("certifications", "certificates", "licenses"),
        "leadership": ("leadership", "leadership experience"),
        "volunteer": ("volunteer experience", "volunteering", "community service"),
        "awards": ("awards", "honors and awards", "honors"),
    }.items():
        value = _section(compact, headings)
        if value:
            suggestions[field] = value
    return suggestions


async def parse_resume_upload(resume: UploadFile) -> tuple[dict[str, str], list[str]]:
    extension = _extension(resume.filename)
    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Upload a PDF, DOCX, or TXT resume.")
    content = await resume.read(MAX_RESUME_BYTES + 1)
    if len(content) > MAX_RESUME_BYTES:
        raise HTTPException(status_code=413, detail="Keep the resume under 2 MB.")
    text = _extract_text(content, extension)
    suggestions = suggestions_from_text(text)
    notes = [
        "These are suggestions only. Review every field before you save your profile or apply.",
        "Your resume is processed locally for this preview and is not saved with your profile.",
    ]
    if not suggestions:
        notes.append("No profile fields were confidently found. You can still fill in the form yourself.")
    return suggestions, notes
