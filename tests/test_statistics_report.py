import json
from pathlib import Path

from src.reporting.statistics_report import StatisticsReport


def test_statistics_report_calculates_average_confidence():
    stats = StatisticsReport()
    stats.candidates_processed = 2
    stats.total_confidence = 1.8
    stats.missing_email = 0
    stats.missing_phone = 0
    stats.missing_experience = 0

    payload = stats.to_dict()

    assert payload["average_confidence"] == 0.9
    assert payload["candidates_processed"] == 2


def test_statistics_report_save_writes_json(tmp_path):
    stats = StatisticsReport()
    stats.candidates_processed = 1
    stats.total_confidence = 0.8
    stats.set_execution_time(0.42)

    output_dir = tmp_path / "output"
    stats.save(str(output_dir))

    saved_file = output_dir / "statistics.json"
    assert saved_file.exists()
    content = json.loads(saved_file.read_text(encoding="utf-8"))
    assert content["execution_time"] == "0.42 sec"
    assert content["average_confidence"] == 0.8
