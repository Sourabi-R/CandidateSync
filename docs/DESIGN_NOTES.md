# Design Document - CandidateSync

## One-Page Architecture & Design

### 📊 Pipeline Overview

```
Input Sources (CSV, PDF)
        │
        ▼
┌──────────────────────────────────────────────┐
│  DETECT: Identify file type & structure     │
└──────────────────┬───────────────────────────┘
                   │
        ▼
┌──────────────────────────────────────────────┐
│  EXTRACT: Parse fields from each source     │
│  - CSV rows → structured fields              │
│  - PDF text → NLP extraction                 │
└──────────────────┬───────────────────────────┘
                   │
        ▼
┌──────────────────────────────────────────────┐
│  NORMALIZE: Standardize formats              │
│  - Phones → E.164                            │
│  - Dates → YYYY-MM                           │
│  - Skills → canonical names                  │
└──────────────────┬───────────────────────────┘
                   │
        ▼
┌──────────────────────────────────────────────┐
│  MERGE: Deduplicate & resolve conflicts      │
│  - Fuzzy match across sources                │
│  - Apply confidence scoring                  │
│  - Track provenance                          │
└──────────────────┬───────────────────────────┘
                   │
        ▼
┌──────────────────────────────────────────────┐
│  PROJECT: Apply runtime config               │
│  - Select subset of fields                   │
│  - Rename/remap fields                       │
│  - Apply per-field normalization             │
└──────────────────┬───────────────────────────┘
                   │
        ▼
┌──────────────────────────────────────────────┐
│  VALIDATE: Schema check                      │
│  - Validate field types                      │
│  - Check required fields                     │
│  - Handle on_missing policy                  │
└──────────────────┬───────────────────────────┘
                   │
        ▼
         Output JSON (canonical profile)
```

---

### 🎯 Canonical Schema

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `candidate_id` | UUID | `550e8400-e29b-41d4-a716-446655440000` | Generated; unique identifier |
| `full_name` | string | `John Doe` | Title case |
| `emails` | string[] | `["john@ex.com"]` | Deduplicated |
| `phones` | string[] | `["+1-415-555-0100"]` | E.164 format |
| `location` | object | `{city: "SF", region: "CA", country: "US"}` | ISO-3166 alpha-2 for country |
| `links` | object | `{linkedin: "...", github: "..."}` | Absolute URIs |
| `headline` | string \| null | `"Senior Engineer"` | Current professional headline |
| `current_company` | string \| null | `"Acme Corp"` | From latest experience |
| `current_title` | string \| null | `"Senior Engineer"` | From latest experience |
| `years_experience` | number \| null | `5` | Calculated from date ranges |
| `experience` | object[] | `[{company, title, start_date, end_date, summary}]` | Chronological order |
| `education` | object[] | `[{institution, degree, field, end_year}]` | Latest first |
| `skills` | object[] | `[{name: "Python", confidence: 0.95}]` | Deduplicated, confidence-scored |
| `provenance` | object[] | `[{field, source, method, raw_value, timestamp}]` | Optional; audit trail |
| `confidence` | object | `{overall: 0.92, by_field: {...}}` | Optional; trust metrics |

---

### 🔄 Merge Strategy

**Primary Source Priority**: CSV > PDF
- CSV is structured, manual entry (higher trust)
- PDF is unstructured, extracted from prose (lower trust)

**Conflict Resolution**:
1. **Exact Match** (fuzzy > 95%): Use with confidence ≥ 0.95
2. **CSV-only Value**: Use CSV with confidence 0.95
3. **PDF-only Value**: Use PDF with confidence 0.85
4. **Conflicting Values**: Use CSV value, set confidence 0.70, log in provenance
5. **Array Fields** (emails, phones, skills): Keep all unique values

**Deduplication**:
- Email/Phone: Case-insensitive, normalize before comparing
- Skills: Fuzzy match against canonical skill list (e.g., "Python", "python3", "Python 3.11" → "Python")

---

### 💪 Confidence Scoring

$$\text{Confidence} = \text{source\_reliability} \times \text{extraction\_confidence} \times \text{normalization\_success}$$

**Source Reliability**:
- CSV: 0.95 (structured, human-entered)
- PDF: 0.85 (unstructured, parsing risk)

**Extraction Confidence**:
- Direct field (e.g., "name" column): 1.0
- Regex/pattern match: 0.80
- Fuzzy match (> 90%): 0.85
- Inferred from context: 0.70

**Normalization Success**:
- Valid format: 1.0
- Partial match (e.g., month guessed): 0.80
- Unable to normalize: null (field omitted)

---

### ⚙️ Runtime Config Projection

```json
{
  "include_provenance": true/false,
  "include_confidence": true/false,
  "on_missing": "null" | "omit" | "error",
  "fields": [
    {
      "path": "output_field_name",
      "from": "canonical_path (e.g., emails[0], skills[].name)",
      "type": "string | number | boolean | object | array",
      "required": true/false,
      "normalize": "E164" | "canonical" | null
    }
  ]
}
```

**Behavior**:
- Selects subset of canonical fields
- Renames/remaps via `from` JSONPath
- Applies per-field normalization
- Handles missing values via `on_missing`
- Validates output schema

---

### ⚠️ Edge Cases & Handling

| Case | Handling |
|------|----------|
| **Missing source file** | Skip; use remaining sources. Confidence < 1.0. |
| **Malformed CSV** | Parse recoverable rows; log & skip broken ones. |
| **Unparseable PDF** | Treat as no data; don't crash. |
| **Conflicting emails** | Keep all; mark conflict in provenance. |
| **Invalid phone format** | Set to null; don't guess country code. |
| **Empty required field + on_missing: "error"** | Fail validation with clear error message. |
| **Circular date range** (end < start) | Set `end_date` to null; log warning. |
| **Duplicate skill names** | Deduplicate; keep highest confidence. |
| **UTF-8 encoding issues** | Decode as UTF-8; replace invalid chars with `?`. |
| **Very old dates** (< 1980) | Accept if valid; flag as likely data error. |
| **Multiple CSV rows for same person** | Merge/deduplicate on fuzzy name match; keep most recent. |

---

### 📋 Implementation Phases

**Phase 1 – Parsing**
- CSV parser (pandas)
- PDF text extractor (pdfplumber)

**Phase 2 – Extraction**
- Field regex patterns (name, email, phone, dates)
- Fuzzy matching for duplicates

**Phase 3 – Normalization**
- Phone normalization (E.164 via `phonenumbers`)
- Date parsing (YYYY-MM via `dateparser`)
- Location mapping (country ISO codes)
- Skill canonicalization (fuzzy list match)

**Phase 4 – Merge & Scoring**
- Candidate deduplication (fuzzy name match)
- Field-level merge logic
- Confidence calculation

**Phase 5 – Projection & Validation**
- JSON config parser
- Field projection (JSONPath)
- Schema validation (pydantic)

**Phase 6 – CLI & Output**
- CLI interface (typer)
- JSON output
- Error handling & logging

---

### 🎯 Success Criteria

- ✅ End-to-end on sample inputs
- ✅ Default + custom config outputs valid
- ✅ Provenance complete & traceable
- ✅ Confidence scores justified (0-1)
- ✅ Edge cases handled gracefully
- ✅ Tests pass with > 80% coverage
- ✅ One-page design PDF (professional)
- ✅ Demo ≤ 2 min, clear

---

**Note**: This is the design foundation. Full technical details will be in the code.

