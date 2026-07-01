import json
from pathlib import Path
from typing import Any

from src.config.constants import DEFAULT_OUTPUT_DIR, STATISTICS_FILE


class StatisticsReport:
    def __init__(self) -> None:
        self.candidates_processed = 0
        self.canonical_profiles = 0
        self.merged_profiles = 0
        self.duplicate_candidates = 0
        self.missing_email = 0
        self.missing_phone = 0
        self.missing_experience = 0
        self.skills_extracted = 0
        self.total_confidence = 0.0
        self.execution_time = 0.0

    def record_candidate(self, profile: Any) -> None:
        self.candidates_processed += 1
        if not getattr(profile, "emails", None):
            self.missing_email += 1
        if not getattr(profile, "phones", None):
            self.missing_phone += 1
        if not getattr(profile, "experience", None):
            self.missing_experience += 1
        self.skills_extracted += len(getattr(profile, "skills", []) or [])
        self.total_confidence += float(getattr(profile, "overall_confidence", 0.0) or 0.0)

    def add_duplicate(self) -> None:
        self.duplicate_candidates += 1

    def set_canonical_profiles(self, count: int) -> None:
        self.canonical_profiles = count

    def set_merged_profiles(self, count: int) -> None:
        self.merged_profiles = count

    def set_execution_time(self, seconds: float) -> None:
        self.execution_time = round(seconds, 2)

    def to_dict(self) -> dict[str, Any]:
        average_confidence = (
            self.total_confidence / self.candidates_processed
            if self.candidates_processed
            else 0.0
        )
        return {
            "candidates_processed": self.candidates_processed,
            "canonical_profiles": self.canonical_profiles,
            "merged_profiles": self.merged_profiles,
            "duplicates_found": self.duplicate_candidates,
            "missing_email": self.missing_email,
            "missing_phone": self.missing_phone,
            "missing_experience": self.missing_experience,
            "skills_extracted": self.skills_extracted,
            "average_confidence": round(average_confidence, 2),
            "execution_time": f"{self.execution_time:.2f} sec",
        }

    def save(self, output_dir: str = DEFAULT_OUTPUT_DIR) -> None:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        file_path = Path(output_dir) / STATISTICS_FILE
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(self.to_dict(), file, indent=4)
