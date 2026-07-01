# CandidateSync

CandidateSync is a configurable multi-source candidate data transformer. It ingests structured recruiter data from CSV and unstructured resume text/PDF content, normalizes and merges them into a canonical profile, scores confidence, tracks provenance, validates output, and projects the result according to runtime config.

## Features

- CSV parser for recruiter data
- PDF resume parser for unstructured candidate content
- Canonical mapping into a shared `CandidateProfile` schema
- Phone normalization to E.164 format
- Merge engine for combining structured and unstructured sources
- Confidence scoring
- Provenance tracking for traceability
- Config-driven output projection
- Output validation before returning results
- Unit tests for core behavior

## Architecture

```text
Recruiter CSV + Resume PDF
        ↓
   Parser Layer
        ↓
 Canonical Mapper
        ↓
  Normalizer / Merger
        ↓
Confidence + Provenance
        ↓
Projection + Validation
        ↓
   JSON Output
```

## Project Structure

```text
CandidateSync/
├── config/                 # Runtime projection configuration
├── input/                  # Sample inputs
├── output/                 # Generated outputs
├── src/
│   ├── cli/                # CLI entrypoint
│   ├── confidence/         # Confidence scoring
│   ├── mapper/             # Canonical mapping
│   ├── merger/             # Merge engine
│   ├── models/             # Pydantic schema
│   ├── normalizer/         # Phone/date/skill normalization
│   ├── parser/             # CSV/PDF parsers
│   ├── projection/         # Config-driven output projection
│   └── validator/          # Output validation
├── tests/                  # Unit tests
└── requirements.txt
```

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 -m src.cli.main \
  --csv input/sample_candidates.csv \
  --resume input/resume.pdf \
  --config config/custom_minimal_config.json
```

## Sample Output

```json
{
  "candidate_name": "John Doe",
  "primary_email": "john.doe@example.com",
  "phone": "+14155550100",
  "experience": 8.0,
  "overall_confidence": 0.86
}
```

## Testing

```bash
pytest -q tests/test_csv_parser.py tests/test_merge_engine.py tests/test_projection.py
```

## Notes

- The project is intentionally designed so that output shape changes from configuration without changing Python code.
- The pipeline is built to be extensible for additional sources such as ATS JSON and recruiter notes.

