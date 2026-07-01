"""Constants used across the CandidateSync pipeline."""
from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = str(PROJECT_ROOT / "output")
CANDIDATE_PROFILE_FILE = "candidate_profile.json"
CANDIDATE_PROFILES_FILE = "candidate_profiles.json"
STATISTICS_FILE = "statistics.json"
CONFLICT_REPORT_FILE = "conflict_report.json"
DUPLICATES_FILE = "duplicates.json"
LOG_FILE = "log.txt"
VERSION = "1.0.0"

DEFAULT_CONFIG_PATH = str(PROJECT_ROOT / "config" / "default_config.json")
CUSTOM_CONFIG_PATH = str(PROJECT_ROOT / "config" / "custom_minimal_config.json")
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_RESUME_EMAIL_REGEX = r"[\w\.-]+@[\w\.-]+\.\w+"
DEFAULT_RESUME_PHONE_REGEX = r"(\+?\d[\d\-\(\) ]{8,}\d)"
DEFAULT_PHONE_REGION = "US"

DEFAULT_CONFIDENCE_WEIGHTS = {
    "field_presence": 0.4,
    "source_reliability": 0.35,
    "normalization_bonus": 0.1,
    "conflict_penalty": 0.15,
}

DEFAULT_SOURCE_RELIABILITY = {
    "csv": 0.95,
    "resume": 0.9,
}

DEFAULT_SOURCE_PRIORITY = {
    "csv": 0.95,
    "resume": 0.9,
}

DATE_INPUT_FORMATS = [
    "%Y-%m",
    "%B %Y",
    "%b %Y",
    "%m/%Y",
    "%Y",
    "%Y/%m",
]
