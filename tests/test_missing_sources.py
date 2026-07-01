import json
from pathlib import Path

from src.parser.resume_parser import ResumeParser
from src.parser.csv_parser import CSVParser


def test_missing_resume_raises_file_not_found():
    parser = ResumeParser("input/missing_resume.txt")

    try:
        parser.parse()
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True


def test_missing_csv_raises_file_not_found():
    parser = CSVParser("input/missing_candidates.csv")

    try:
        parser.parse()
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True
