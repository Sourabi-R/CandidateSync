from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.config.constants import DEFAULT_OUTPUT_DIR, DUPLICATES_FILE
from src.normalizer.phone_normalizer import PhoneNormalizer
from src.utils.validators import is_valid_email


class DuplicatesReport:
    """Detect and report duplicate recruiter records."""

    def __init__(self) -> None:
        self.duplicates_found = 0
        self.merged_profiles = 0
        self.duplicate_candidates: list[dict[str, Any]] = []
        self.groups: dict[str, list[dict[str, Any]]] = {}

    def detect(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for record in records:
            key = self._duplicate_key(record)
            grouped[key].append(record)

        self.groups = grouped
        self.duplicates_found = sum(len(records) - 1 for records in grouped.values() if len(records) > 1)
        self.merged_profiles = len(grouped)
        self.duplicate_candidates = []

        for key, records_group in grouped.items():
            if len(records_group) > 1:
                record = records_group[0]
                matched_on = "email" if record.get("email") else "phone" if record.get("phone") else "name"
                self.duplicate_candidates.append(
                    {
                        "candidate": record.get("name") or record.get("full_name"),
                        "matched_on": matched_on,
                        "email": record.get("email"),
                        "phone": record.get("phone"),
                    }
                )

        return [self._merge_records(records) for records in grouped.values()]

    def _duplicate_key(self, record: dict[str, Any]) -> str:
        email = record.get("email")
        if email and is_valid_email(email):
            return f"email::{email.strip().lower()}"

        normalized_phone = PhoneNormalizer.normalize(record.get("phone"))
        if normalized_phone:
            return f"phone::{normalized_phone}"

        name = record.get("name") or record.get("full_name")
        if name:
            return f"name::{name.strip().lower()}"

        return f"record::{id(record)}"

    def _merge_records(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        merged: dict[str, Any] = {}
        for record in records:
            for key, value in record.items():
                if value is None or value == "":
                    continue
                if key not in merged or merged[key] in (None, ""):
                    merged[key] = value
                    continue
                if key == "skills":
                    normalized = set(merged[key] or []) | set(value or [])
                    merged[key] = sorted(normalized)
        return merged

    def save(self, output_dir: str = DEFAULT_OUTPUT_DIR) -> None:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_path = Path(output_dir) / DUPLICATES_FILE
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(
                {
                    "duplicates_found": self.duplicates_found,
                    "merged_profiles": self.merged_profiles,
                    "duplicate_candidates": self.duplicate_candidates,
                },
                file,
                indent=4,
            )
