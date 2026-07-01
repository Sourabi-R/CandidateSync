from src.normalizer.date_normalizer import normalize_date


def test_date_normalizer_handles_month_year_formats():
    assert normalize_date("Jan 2024") == "2024-01"
    assert normalize_date("January 2024") == "2024-01"
    assert normalize_date("01/2024") == "2024-01"
    assert normalize_date("2024") == "2024-01"
    assert normalize_date("2024/06") == "2024-06"


def test_date_normalizer_returns_text_when_unknown():
    assert normalize_date("Q1 2024") == "Q1 2024"
