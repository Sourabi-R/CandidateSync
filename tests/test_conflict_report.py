import json
from pathlib import Path

from src.reporting.conflict_report import ConflictReport


def test_conflict_report_add_and_save(tmp_path):
    report = ConflictReport()
    report.add(
        field="current_title",
        csv_value="Engineer",
        resume_value="Senior Engineer",
        selected="Engineer",
        reason="CSV confidence higher",
        winning_source="csv",
        confidence=0.95,
    )

    output_dir = tmp_path / "output"
    report.save(str(output_dir))

    file_path = output_dir / "conflict_report.json"
    assert file_path.exists()
    content = json.loads(file_path.read_text(encoding="utf-8"))
    assert content[0]["field"] == "current_title"
