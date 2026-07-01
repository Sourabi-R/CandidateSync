````md
# 🚀 CandidateSync

## Multi-Source Candidate Data Transformer

**Python • CLI • JSON Configuration • Pydantic • Pytest**

A production-ready candidate data transformation pipeline that consolidates fragmented candidate information from multiple structured and unstructured sources into a single canonical candidate profile.

---

# 📌 Overview

CandidateSync was developed as part of the **Eightfold Engineering Internship Assignment**.

The system transforms recruiter CSV files and resume documents into a single canonical candidate profile by performing:

- 📂 Multi-source data ingestion
- 🔄 Data normalization
- 👥 Duplicate detection
- ⚖️ Conflict resolution
- 📊 Confidence calculation
- 📍 Provenance tracking
- ⚙️ Runtime configurable output
- ✅ Schema validation

---

# ✨ Features

## 📂 Multi-Source Input

### Structured Sources

- ✅ Recruiter CSV

### Unstructured Sources

- ✅ Resume (.txt)

---

## 📋 Canonical Candidate Profile

Each generated profile contains:

- Candidate ID
- Full Name
- Emails
- Phone Numbers
- Location
- Headline
- Current Company
- Current Title
- Years of Experience
- Skills
- Experience
- Education
- Provenance
- Confidence Score

---

## 🔄 Processing Pipeline

```text
Recruiter CSV + Resume
        │
        ▼
Data Extraction
        │
        ▼
Data Parsing
        │
        ▼
Canonical Mapping
        │
        ▼
Normalization
        │
        ▼
Merge Engine
        │
        ▼
Conflict Resolution
        │
        ▼
Confidence Calculation
        │
        ▼
Runtime Projection
        │
        ▼
Schema Validation
        │
        ▼
JSON Output
````

---

# ⚙️ Normalization

CandidateSync automatically performs:

* 📞 Phone Normalization (E.164)
* 📅 Date Normalization (YYYY-MM)
* 🧠 Skill Canonicalization
* 📧 Email Validation
* 🔁 Duplicate Removal
* 📍 Location Standardization

---

# 🔀 Merge Strategy

Candidate records are matched using:

* Email Address
* Phone Number
* Candidate Name

Priority Rules:

| Field           | Preferred Source |
| --------------- | ---------------- |
| Employment      | Recruiter CSV    |
| Skills          | Resume           |
| Contact Details | Recruiter CSV    |

Every selected field records:

* Source
* Extraction Method
* Confidence

---

# 🎯 Runtime Configurable Output

The runtime JSON configuration supports:

* ✅ Select Fields
* ✅ Rename Fields
* ✅ Remap Canonical Paths
* ✅ Toggle Provenance
* ✅ Toggle Confidence
* ✅ Missing Value Policy
* ✅ Schema Validation

---

# 📊 Generated Outputs

The pipeline generates:

* 📄 candidate_profile.json
* 📄 candidate_profiles.json
* 📈 statistics.json
* 🔁 duplicates.json
* ⚠️ conflict_report.json
* 📝 log.txt

---

# 🏗️ System Architecture

```text
Recruiter CSV        Resume TXT
      │                   │
      └────────┬──────────┘
               ▼
       Data Extraction
               │
               ▼
      Canonical Mapping
               │
               ▼
      Data Normalization
               │
               ▼
         Merge Engine
               │
               ▼
    Conflict Resolution
               │
               ▼
    Confidence Assignment
               │
               ▼
     Runtime Projection
               │
               ▼
      Schema Validation
               │
               ▼
      JSON Output Files
```

---

# 🛠️ Technology Stack

| Technology  | Purpose               |
| ----------- | --------------------- |
| Python 3.11 | Backend               |
| Pydantic    | Validation            |
| JSON        | Runtime Configuration |
| CSV         | Structured Input      |
| Logging     | Pipeline Monitoring   |
| Pytest      | Automated Testing     |
| Git         | Version Control       |
| GitHub      | Repository Hosting    |

---

# 📂 Project Structure

```text
CandidateSync/

├── config/
├── docs/
├── input/
├── output/
├── scripts/
├── src/
├── tests/
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/Sourabi-R/CandidateSync.git

cd CandidateSync
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv311

.venv311\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv311

source .venv311/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Pipeline

### Default Output

```bash
python -m src.cli.main \
--csv input/sample_candidates.csv \
--resume input/resume.txt \
--config config/default_config.json
```

### Custom Output

```bash
python -m src.cli.main \
--csv input/sample_candidates.csv \
--resume input/resume.txt \
--config config/custom_minimal_config.json
```

---

# 🧪 Run Tests

```bash
pytest -q
```

Expected Output

```text
25 passed
```

---

# 📦 Output Files

```text
output/

candidate_profile.json

candidate_profiles.json

statistics.json

duplicates.json

conflict_report.json

log.txt
```

---

# 🎯 Assignment Coverage

| Requirement         | Status |
| ------------------- | ------ |
| Structured Source   | ✅      |
| Unstructured Source | ✅      |
| Canonical Schema    | ✅      |
| Runtime Config      | ✅      |
| Normalization       | ✅      |
| Merge Engine        | ✅      |
| Conflict Resolution | ✅      |
| Confidence          | ✅      |
| Provenance          | ✅      |
| Validation          | ✅      |
| CLI                 | ✅      |
| Reports             | ✅      |
| Tests               | ✅      |

---

# 🔮 Future Enhancements

* ATS JSON Support
* LinkedIn Integration
* GitHub Profile Integration
* PDF Resume Parsing
* DOCX Resume Parsing
* Semantic Skill Matching
* AI Entity Resolution
* Web Dashboard
* REST API
* Cloud Deployment

---

# 👩‍💻 Author

**Sourabi R**

B.Tech Artificial Intelligence & Data Science

**Eightfold Engineering Internship Assignment (Jul–Dec 2026)**

---

# ⭐ CandidateSync

**A configurable, explainable and production-ready Multi-Source Candidate Data Transformation Pipeline.**

```

This structure is almost identical to the polished AI-HRMS README style and renders cleanly on GitHub with proper spacing, headings, tables, code blocks, and emojis.
```
