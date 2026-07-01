import re
from pathlib import Path
from typing import Any

import pdfplumber

from src.normalizer.phone_normalizer import PhoneNormalizer
from src.utils.validators import is_valid_email


class PDFResumeParser:
    """Parser for PDF resumes."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def parse(self) -> dict[str, Any]:
        """Extract candidate information from a PDF resume file."""
        path = Path(self.file_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume not found: {path}")

        text = ""
        try:
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as error:
            raise ValueError(f"PDF parsing failed: {error}") from error

        candidate: dict[str, Any] = {}
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        candidate["name"] = lines[0] if lines else None

        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        email_value = email_match.group(0) if email_match else None
        candidate["email"] = email_value if is_valid_email(email_value) else None

        phone_match = re.search(r"(\+?\d[\d\-\(\) ]{8,}\d)", text)
        candidate["phone"] = PhoneNormalizer.normalize(phone_match.group(0)) if phone_match else None

        skills: list[str] = []
        predefined = [
            "Python",
            "Java",
            "SQL",
            "Docker",
            "Kubernetes",
            "AWS",
            "React",
            "Node.js",
            "JavaScript",
            "C++",
        ]
        lowercase_text = text.lower()
        for skill in predefined:
            if skill.lower() in lowercase_text:
                skills.append(skill)

        candidate["skills"] = skills
        return candidate
