import json
from pathlib import Path

from src.config.constants import CONFLICT_REPORT_FILE, DEFAULT_OUTPUT_DIR


class ConflictReport:

    def __init__(self):
        self.conflicts: list[dict[str, str | None]] = []

    def add(
        self,
        field: str,
        csv_value: str | None,
        resume_value: str | None,
        selected: str | None,
        reason: str,
        winning_source: str = "csv",
        confidence: float = 0.0,
    ) -> None:
        self.conflicts.append({
            "field": field,
            "csv_value": csv_value,
            "resume_value": resume_value,
            "selected_value": selected,
            "winning_source": winning_source.upper(),
            "reason": reason,
            "confidence": round(confidence, 2),
        })

    def save(self, output_dir: str = DEFAULT_OUTPUT_DIR) -> None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        file_path = output_path / CONFLICT_REPORT_FILE
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(self.conflicts, file, indent=4)
