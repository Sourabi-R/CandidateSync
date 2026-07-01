from src.parser.csv_parser import CSVParser


def test_csv_parser_reads_sample_candidates():
    parser = CSVParser("input/sample_candidates.csv")
    rows = parser.parse()

    assert len(rows) > 0
    assert rows[0]["name"] == "John Doe"
