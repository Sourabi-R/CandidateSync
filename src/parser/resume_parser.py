import re
from pathlib import Path
from typing import Any

from src.normalizer.date_normalizer import normalize_date
from src.normalizer.phone_normalizer import PhoneNormalizer
from src.normalizer.skill_normalizer import normalize_skills
from src.utils.validators import is_valid_email


def _extract_field(text: str, labels: list[str]) -> str | None:
    for label in labels:
        pattern = rf"{re.escape(label)}\s*[:\-]\s*(.+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _extract_section(text: str, heading: str) -> str | None:
    pattern = rf"{re.escape(heading)}\s*[:\-]?\s*(.+?)(?:\n\n|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        section = match.group(1).strip()
        return " ".join(line.strip() for line in section.splitlines() if line.strip())
    return None


def _extract_experience_block(text: str) -> dict[str, str | None]:
    match = re.search(r"Experience\s*(?:\n|\r\n)(.+?)(?:\n\n|Education|$)", text, re.IGNORECASE | re.DOTALL)
    if not match:
        return {}

    lines = [line.strip() for line in match.group(1).splitlines() if line.strip()]
    experience = {}
    if lines:
        experience["company"] = lines[0]
    if len(lines) > 1:
        experience["title"] = lines[1]
    if len(lines) > 2:
        experience["summary"] = " ".join(lines[2:])
    return experience


def _find_date_range(text: str) -> tuple[str | None, str | None]:
    match = re.search(
        r"(?P<start>[A-Za-z]{3,9}\s+\d{4}|\d{1,2}/\d{4}|\d{4})\s*[-–]\s*(?P<end>Present|Current|[A-Za-z]{3,9}\s+\d{4}|\d{1,2}/\d{4}|\d{4})",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None, None
    start = normalize_date(match.group("start"))
    end = normalize_date(match.group("end"))
    return start, end


def _contains_contact_line(line: str) -> bool:
    return bool(re.search(r"@|\+?\d", line)) or bool(re.search(r"location\s*[:\-]", line, re.IGNORECASE))


class ResumeParser:
    """Parser for resume text files."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def parse(self) -> dict[str, Any]:
        """Read resume text and return extracted candidate fields."""
        path = Path(self.file_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume not found: {path}")

        try:
            text = path.read_text(encoding="utf-8")
        except Exception as error:
            raise ValueError(f"Resume parsing failed: {error}") from error

        candidate: dict[str, Any] = {}
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        email_value = email_match.group(0) if email_match else None
        candidate["email"] = email_value if is_valid_email(email_value) else None

        phone_match = re.search(r"(\+?\d[\d\-\(\) ]{8,}\d)", text)
        candidate["phone"] = PhoneNormalizer.normalize(phone_match.group(0)) if phone_match else None

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        candidate["name"] = lines[0] if lines else None

        candidate["headline"] = _extract_field(text, ["headline", "professional summary", "summary", "title", "role"])
        candidate["location"] = _extract_field(text, ["location"])
        candidate["current_company"] = _extract_field(text, ["current company", "company", "employer"])
        candidate["current_title"] = _extract_field(text, ["current title", "title", "role"])
        candidate["experience_summary"] = _extract_section(text, "Experience Summary") or _extract_section(text, "Professional Experience") or _extract_section(text, "Summary")

        if not candidate["headline"] and len(lines) > 1 and not _contains_contact_line(lines[1]):
            candidate["headline"] = lines[1]

        experience_block = _extract_experience_block(text)
        if experience_block.get("company") and not candidate.get("current_company"):
            candidate["current_company"] = experience_block["company"]
        if experience_block.get("title") and not candidate.get("current_title"):
            candidate["current_title"] = experience_block["title"]
        if experience_block.get("summary") and not candidate.get("experience_summary"):
            candidate["experience_summary"] = experience_block["summary"]

        if not candidate["current_title"] and not candidate["current_company"]:
            match = re.search(r"(?P<title>\b[\w ]+(Engineer|Developer|Manager|Consultant|Analyst|Architect)\b)\s+at\s+(?P<company>[A-Za-z0-9 &]+)", text, re.IGNORECASE)
            if match:
                candidate["current_title"] = match.group("title").strip()
                candidate["current_company"] = match.group("company").strip()

        experience_entry: dict[str, Any] = {}
        if candidate.get("current_company"):
            experience_entry["company"] = candidate["current_company"]
        if candidate.get("current_title"):
            experience_entry["title"] = candidate["current_title"]
        if candidate.get("experience_summary"):
            experience_entry["summary"] = candidate["experience_summary"]

        start_date, end_date = _find_date_range(text)
        if start_date:
            experience_entry["start"] = start_date
        if end_date:
            experience_entry["end"] = end_date

        candidate["experience"] = [experience_entry] if experience_entry else []

        skill_aliases = [
            "python",
            "py",
            "javascript",
            "js",
            "java script",
            "java",
            "sql",
            "docker",
            "kubernetes",
            "aws",
            "react",
            "node",
            "node.js",
            "nodejs",
            "c++",
            "c#",
        ]
        lowercase_text = text.lower()
        detected_skills: list[str] = []
        for alias in skill_aliases:
            pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
            if re.search(pattern, lowercase_text):
                detected_skills.append(alias)

        candidate["skills"] = normalize_skills(detected_skills)
        return candidate
