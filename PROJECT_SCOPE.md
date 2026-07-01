# CandidateSync – Project Scope & Planning

**Project Name**: CandidateSync

**Assignment**: Eightfold Engineering Intern – Multi-Source Candidate Data Transformer

**Start Date**: June 30, 2026

---

## 🎯 Objectives

Transform messy, multi-source candidate data into one canonical, trustworthy profile with:

1. **Data Consolidation**: Merge overlapping/conflicting values from multiple sources
2. **Normalization**: Standardize dates, phones, locations, skills
3. **Provenance Tracking**: Record where each value came from
4. **Confidence Scoring**: Rate how trustworthy each field is
5. **Schema Validation**: Ensure outputs match expected structure
6. **Graceful Degradation**: Handle missing/garbage data without crashing
7. **Runtime Flexibility**: Allow custom output schemas via configuration

---

## 📊 Source Types Selected

### ✅ Structured Source: Recruiter CSV

**Why**: Easy to parse, well-defined structure, representative of real recruiter data.

**Fields**:
- Name
- Email
- Phone
- Current Company
- Current Title
- Years of Experience (optional)

**Format**:
```csv
name,email,phone,current_company,current_title,years_experience
John Doe,john.doe@example.com,+1-415-555-0100,Acme Corp,Senior Engineer,5
```

---

### ✅ Unstructured Source: Resume PDF

**Why**: Realistic, contains rich information, requires intelligent extraction.

**Contains**:
- Contact information (name, email, phone, location)
- Professional summary
- Work experience (company, title, dates, description)
- Education (school, degree, field, graduation year)
- Skills
- Links (portfolio, GitHub, LinkedIn)

**Format**: Free-text PDF prose (parsed via pdfplumber)

---

## 🏗️ Canonical Profile Schema

```json
{
  "candidate_id": "uuid",
  "full_name": "string",
  "emails": ["string"],
  "phones": ["string"],
  "location": {
    "city": "string | null",
    "region": "string | null",
    "country": "string (ISO-3166 alpha-2)"
  },
  "links": {
    "linkedin": "url | null",
    "github": "url | null",
    "portfolio": "url | null",
    "other": ["url"]
  },
  "headline": "string | null",
  "current_company": "string | null",
  "current_title": "string | null",
  "years_experience": "number | null",
  "experience": [
    {
      "company": "string",
      "title": "string",
      "start_date": "YYYY-MM",
      "end_date": "YYYY-MM | null",
      "summary": "string | null"
    }
  ],
  "education": [
    {
      "institution": "string",
      "degree": "string | null",
      "field": "string | null",
      "end_year": "YYYY | null"
    }
  ],
  "skills": [
    {
      "name": "string (canonical)",
      "confidence": "number (0-1)"
    }
  ],
  "provenance": [
    {
      "field": "string",
      "source": "recruiter_csv | resume_pdf",
      "method": "string",
      "raw_value": "any",
      "timestamp": "ISO-8601"
    }
  ],
  "confidence": {
    "overall": "number (0-1)",
    "by_field": {
      "field_name": "number (0-1)"
    }
  }
}
```

---

## 📏 Normalization Strategy

| Field | Format | Method |
|-------|--------|--------|
| **Phones** | E.164 (`+1-415-555-0100`) | `phonenumbers` library |
| **Dates** | `YYYY-MM` | `dateparser` + validation |
| **Countries** | ISO-3166 alpha-2 (`US`, `CA`, `UK`) | Mapping table |
| **Skills** | Canonical names (see mapping) | Fuzzy match + manual list |
| **URLs** | Absolute URIs | Regex validation |
| **Names** | Title case | Simple `.title()` + cleanup |

---

## 🔀 Merge & Conflict Resolution

When the same field appears in multiple sources with different values:

1. **Exact Match**: If values are identical (fuzzy match > 95%), use it with high confidence.
2. **Primary Source Priority**: Recruiter CSV is more structured; use it as primary.
3. **Fallback**: Use Resume PDF to fill gaps.
4. **Conflict**: If values conflict, pick the more reliable source and log confidence < 0.8.
5. **Array Deduplication**: For emails/phones/skills, deduplicate and keep all unique values.

---

## 💪 Confidence Scoring

```
confidence = (source_reliability × field_extraction_confidence × normalization_success) × deduplication_factor

source_reliability:
  - recruiter_csv:   0.95 (structured, manual entry)
  - resume_pdf:      0.85 (unstructured, OCR/parsing risk)

field_extraction_confidence:
  - direct_field:    1.0 (found exactly)
  - fuzzy_matched:   0.85 (fuzzy string match > 90%)
  - inferred:        0.70 (inferred from context)
  - pattern_matched: 0.80 (regex pattern)

normalization_success:
  - valid:           1.0
  - partial:         0.80 (partial match, e.g., month guessed)
  - unknown:         null (can't normalize)

deduplication_factor:
  - unique:          1.0 (only one source)
  - merged:          0.95 (merged, sources agree)
  - conflicted:      0.70 (sources disagree, picked winner)
```

---

## ⚙️ Runtime Configuration

Users can reshape output via JSON config:

```json
{
  "fields": [
    {
      "path": "full_name",
      "from": "full_name",
      "type": "string",
      "required": true,
      "normalize": null
    },
    {
      "path": "primary_email",
      "from": "emails[0]",
      "type": "string",
      "required": true,
      "normalize": "email"
    },
    {
      "path": "phone",
      "from": "phones[0]",
      "type": "string",
      "required": false,
      "normalize": "E164"
    },
    {
      "path": "skills",
      "from": "skills[].name",
      "type": "string[]",
      "required": false,
      "normalize": "canonical"
    }
  ],
  "include_provenance": false,
  "include_confidence": true,
  "on_missing": "null"
}
```

---

## ⚠️ Edge Cases

| Case | Handling |
|------|----------|
| **Missing source** | Skip it; use remaining sources. Output confidence < 1.0. |
| **Malformed CSV** | Log error, parse recoverable rows, skip broken ones. |
| **Unparseable PDF** | Treat as no data; don't crash. |
| **Conflicting emails** | Keep all; mark conflict in provenance. |
| **Invalid phone** | Set to `null`; don't guess country code. |
| **Empty required field** | If `on_missing: "error"`, fail validation; else `null`. |
| **Circular date ranges** | Set `end_date` to `null`; flag as warning. |
| **Duplicate skill names** | Deduplicate; keep highest confidence version. |
| **Encoding issues** | Decode as UTF-8; replace invalid chars with `?`. |
| **Very old dates** | Accept if valid; flag if < 1980 as likely error. |

---

## 🎯 Pipeline Steps

```
┌─────────────────┐
│   Input Files   │ (CSV, PDF)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Detect      │ (File type, format validation)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     Extract     │ (Parse CSV rows, extract text from PDF)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Normalize     │ (Dates, phones, locations, skills)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      Merge      │ (Deduplicate, conflict-resolve, confidence score)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Project      │ (Apply runtime config, reshape schema)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Validate     │ (Schema check, required fields)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Output       │ (JSON + provenance/confidence)
└─────────────────┘
```

---

## 📋 Scope: What's Included

- ✅ Recruiter CSV parsing
- ✅ Resume PDF extraction
- ✅ Phone normalization (E.164)
- ✅ Date normalization (YYYY-MM)
- ✅ Merge logic with confidence scoring
- ✅ Provenance tracking
- ✅ Runtime config projection
- ✅ Schema validation
- ✅ CLI interface
- ✅ Unit tests with edge cases

---

## 🚫 Scope: What's Excluded (Time Pressure Cutoffs)

- ❌ GitHub profile URL parsing (requires API, authentication)
- ❌ LinkedIn profile URL parsing (requires scraping/API)
- ❌ Recruiter notes (.txt) parsing (NLP-heavy, high complexity)
- ❌ Web UI dashboard (CLI is sufficient)
- ❌ Database persistence (JSON file output is enough)
- ❌ Real-time streaming (batch processing only)
- ❌ Advanced ML deduplication (fuzzy matching is enough)
- ❌ Full PDF OCR (pdfplumber text extraction only)

---

## 📈 Success Criteria

- [ ] Code runs end-to-end on sample inputs
- [ ] Default schema JSON is valid
- [ ] Custom config outputs match requested schema
- [ ] Provenance is complete & traceable
- [ ] Confidence scores are reasonable (0-1, justified)
- [ ] Edge cases handled gracefully
- [ ] Tests pass with > 80% code coverage
- [ ] Design PDF is one page, professional
- [ ] Demo video is ≤ 2 minutes, clear

---

## 📅 Phases

| Phase | Task | Duration |
|-------|------|----------|
| **1** | Design (architecture PDF) | 4 hours |
| **2** | Implementation (code) | 8 hours |
| **3** | Testing & refinement | 4 hours |
| **4** | Demo & documentation | 2 hours |

**Total**: ~18 hours

---

## ✅ Checkpoint: Step 1 Complete

By completing this scope document, you've:

- ✅ Selected sources (Recruiter CSV + Resume PDF)
- ✅ Defined canonical schema
- ✅ Planned normalization strategy
- ✅ Designed merge & confidence logic
- ✅ Identified edge cases
- ✅ Scoped the work realistically

**Next Step**: Build the one-page design PDF.

