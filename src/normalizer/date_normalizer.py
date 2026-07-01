"""Date normalization utilities."""

import re
from datetime import datetime

from src.config.constants import DATE_INPUT_FORMATS


def normalize_date(value: str) -> str:
    """Normalize a date string into an ISO year-month string."""
    if not value or not value.strip():
        return ""

    text = value.strip()
    if text.lower() in {"present", "current"}:
        return None

    for date_format in DATE_INPUT_FORMATS:
        try:
            parsed = datetime.strptime(text, date_format)
            if date_format == "%Y":
                return f"{parsed.year}-01"
            return parsed.strftime("%Y-%m")
        except ValueError:
            continue

    month_match = re.match(r"^(?P<month>[A-Za-z]+)\s+(?P<year>\d{4})$", text)
    if month_match:
        try:
            parsed = datetime.strptime(text, "%B %Y")
            return parsed.strftime("%Y-%m")
        except ValueError:
            try:
                parsed = datetime.strptime(text, "%b %Y")
                return parsed.strftime("%Y-%m")
            except ValueError:
                pass

    year_match = re.match(r"^(?P<year>\d{4})$", text)
    if year_match:
        return f"{year_match.group('year')}-01"

    return text
