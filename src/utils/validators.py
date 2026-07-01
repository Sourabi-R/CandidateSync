import re
from typing import Pattern

from src.config.constants import DEFAULT_RESUME_EMAIL_REGEX

EMAIL_PATTERN: Pattern[str] = re.compile(DEFAULT_RESUME_EMAIL_REGEX)


def is_valid_email(email: str | None) -> bool:
    """Return True when the provided email address is a valid format."""
    if not email:
        return False
    return bool(EMAIL_PATTERN.fullmatch(email.strip()))
