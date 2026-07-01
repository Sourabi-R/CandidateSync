from src.parser.resume_parser import ResumeParser


def test_resume_parser_extracts_data_from_sample_resume():
    parser = ResumeParser("input/resume.txt")
    candidate = parser.parse()

    assert candidate["email"] == "john.doe@example.com"
    assert candidate["phone"] == "+14155550100"
    assert candidate["headline"] == "Senior Software Engineer"
    assert candidate["location"] == "San Francisco, CA, USA"
    assert "Python" in candidate["skills"]
    assert candidate["current_company"] == "Acme Corp"
    assert candidate["current_title"] == "Senior Software Engineer"


def test_resume_parser_handles_missing_fields(tmp_path, monkeypatch):
    fake_file = tmp_path / "empty_resume.txt"
    fake_file.write_text("\n\n")

    parser = ResumeParser(str(fake_file))
    candidate = parser.parse()

    assert candidate["email"] is None
    assert candidate["phone"] is None
    assert candidate["skills"] == []
