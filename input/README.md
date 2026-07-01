# Sample Inputs

This directory contains sample data that will be used to test the CandidateSync pipeline.

## Files

### `sample_candidates.csv`

A Recruiter CSV export with structured candidate data.

**Format**: CSV with headers
- `name`: Candidate full name
- `email`: Email address
- `phone`: Phone number (various formats)
- `current_company`: Current employer
- `current_title`: Current job title
- `years_experience`: Years of professional experience (optional)

**Example**:
```
name,email,phone,current_company,current_title,years_experience
John Doe,john.doe@example.com,+1-415-555-0100,Acme Corp,Senior Software Engineer,8
```

### `sample_resume.pdf` (to be created)

A sample Resume PDF with unstructured data:
- Contact information
- Professional summary
- Work experience (company, title, dates, description)
- Education
- Skills
- Links

---

## Usage

These inputs will be processed by the CandidateSync pipeline:

```bash
python -m src.cli transform --input input/ --output output/default.json
```

**Expected Output**: `output/default.json` (canonical profile with provenance & confidence)

