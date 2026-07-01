from typing import Any

from src.models.schema import CandidateProfile, Experience, Location
from src.normalizer.phone_normalizer import PhoneNormalizer
from src.utils.validators import is_valid_email

STATE_ABBREVIATIONS = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

COUNTRY_ALIASES = {
    "usa": "US",
    "us": "US",
    "united states": "US",
    "united states of america": "US",
}


def _parse_location(value: str) -> Location:
    if not value:
        return Location()

    parts = [part.strip() for part in value.split(",") if part.strip()]
    city = parts[0] if parts else None
    region = None
    country = None

    if len(parts) > 1:
        normalized_region = parts[1].upper()
        region = STATE_ABBREVIATIONS.get(normalized_region, parts[1].title())

    if len(parts) > 2:
        normalized_country = parts[2].strip().lower()
        country = COUNTRY_ALIASES.get(normalized_country, parts[2].upper())

    return Location(city=city, region=region, country=country)


class CanonicalMapper:
    """Map recruiter CSV records into the canonical candidate profile."""

    @staticmethod
    def map_csv(candidate: dict[str, Any]) -> CandidateProfile:
        candidate_id = candidate.get("candidate_id") or candidate.get("email") or "unknown"
        email_value = candidate.get("email")
        emails = [email_value] if email_value and is_valid_email(email_value) else []

        phone_value = candidate.get("phone")
        normalized_phone = PhoneNormalizer.normalize(phone_value)
        phones: list[str] = [normalized_phone] if normalized_phone else []

        experience = [
            Experience(
                company=candidate.get("current_company"),
                title=candidate.get("current_title"),
                summary=candidate.get("experience_summary"),
            )
        ] if candidate.get("current_company") or candidate.get("current_title") or candidate.get("experience_summary") else []

        years_experience = None
        if candidate.get("years_experience") is not None:
            try:
                years_experience = float(candidate["years_experience"])
            except (TypeError, ValueError):
                years_experience = None

        location = None
        if candidate.get("location"):
            location = _parse_location(candidate["location"])

        return CandidateProfile(
            candidate_id=candidate_id,
            full_name=candidate.get("name") or candidate.get("full_name"),
            emails=emails,
            phones=phones,
            location=location,
            headline=candidate.get("headline"),
            current_company=candidate.get("current_company"),
            current_title=candidate.get("current_title"),
            experience_summary=candidate.get("experience_summary"),
            years_experience=years_experience,
            experience=experience,
        )
