import json
from pathlib import Path

from src.reporting.duplicates_report import DuplicatesReport


def test_duplicates_report_detects_duplicate_records():
    records = [
        {"name": "John Doe", "email": "john@example.com", "phone": "+14155550100"},
        {"name": "John Doe", "email": "john@example.com", "phone": "415-555-0100"},
    ]

    report = DuplicatesReport()
    merged = report.detect(records)

    assert report.duplicates_found == 1
    assert len(merged) == 1


def test_duplicates_report_save_writes_json(tmp_path):
    report = DuplicatesReport()
    report.groups = {"email::john@example.com": [{"name": "John Doe"}, {"name": "John Doe"}]}
    report.duplicates_found = 1
    report.merged_profiles = 1

    output_dir = tmp_path / "output"
    report.save(str(output_dir))

    content = json.loads((output_dir / "duplicates.json").read_text(encoding="utf-8"))
    assert content["duplicates_found"] == 1
    assert content["merged_profiles"] == 1
