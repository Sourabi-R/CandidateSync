🚀 CandidateSync
Multi-Source Candidate Data Transformer

Python • CLI • JSON Configuration • Pydantic • Pytest

A production-ready candidate data transformation pipeline that consolidates fragmented candidate information from multiple structured and unstructured sources into a single canonical profile. The system performs normalization, deduplication, conflict resolution, confidence scoring, provenance tracking, and configurable output generation for downstream recruitment systems.

📌 Overview

CandidateSync is designed to solve one of the biggest challenges in modern recruitment systems—combining candidate information from multiple sources into one reliable profile.

The pipeline ingests recruiter CSV exports and resume files, transforms them into a standardized schema, resolves conflicting information, tracks data provenance, assigns confidence scores, and generates validated JSON outputs that can be easily consumed by ATS and hiring platforms.

The system helps organizations:

📂 Consolidate candidate data from multiple sources
🔄 Normalize inconsistent information
👥 Merge duplicate candidate records
⚖️ Resolve conflicting candidate details
📊 Calculate confidence scores
📍 Track provenance for every field
⚙️ Generate configurable output using runtime JSON configuration
✅ Produce schema-valid outputs for downstream systems
✨ Features
📂 Multi-Source Data Processing
Structured Source
Recruiter CSV Export
Unstructured Source
Resume (.txt)
📋 Canonical Candidate Profile

Each candidate profile includes

Candidate ID
Full Name
Emails
Phone Numbers
Location
Headline
Current Company
Current Title
Years of Experience
Experience History
Education
Skills
Provenance
Confidence Score
🔄 Data Processing Pipeline
Recruiter CSV
Resume TXT
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
 Data Normalization
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
 JSON Output Generation
⚙️ Data Normalization

CandidateSync automatically performs

📞 Phone Number Normalization (E.164)
📅 Date Standardization (YYYY-MM)
🧠 Canonical Skill Mapping
📧 Email Validation
🔁 Duplicate Removal
📍 Location Normalization
📑 Consistent Candidate Schema
🔀 Merge & Conflict Resolution

Candidate records are matched using

Email Address
Phone Number
Candidate Name

Conflict resolution uses predefined source-priority rules.

Candidate Field	Preferred Source
Employment Details	Recruiter CSV
Skills	Resume
Contact Information	Recruiter CSV

Every populated field records

Source
Extraction Method
Confidence

ensuring complete explainability.

🎯 Runtime Configurable Output

Without changing the application code, CandidateSync supports runtime JSON configurations to

Select output fields
Rename fields
Remap canonical attributes
Enable / Disable Provenance
Enable / Disable Confidence
Configure Missing Value Handling
Validate Output Schema

Example

{
  "fields": [
    {
      "path": "candidate_name",
      "from": "full_name"
    },
    {
      "path": "primary_email",
      "from": "emails[0]"
    }
  ]
}
📊 Pipeline Outputs

The pipeline automatically generates

📄 candidate_profile.json
📄 candidate_profiles.json
📈 statistics.json
🔁 duplicates.json
⚠️ conflict_report.json
📝 log.txt
📊 Pipeline Summary

After every successful execution

Candidates Processed : 3

Canonical Profiles   : 3

Duplicates Found     : 0

Average Confidence   : 0.54

Execution Time       : 0.09 sec
🏗️ System Architecture
                 Recruiter CSV
                        │
                        ▼
                 CSV Parser
                        │
                        ▼
                  Resume TXT
                        │
                        ▼
                 Resume Parser
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 Canonical Mapper                 Normalization
        │                               │
        └───────────────┬───────────────┘
                        ▼
                  Merge Engine
                        │
                        ▼
             Conflict Resolution
                        │
                        ▼
           Confidence Calculator
                        │
                        ▼
          Runtime JSON Projection
                        │
                        ▼
             Schema Validation
                        │
                        ▼
               JSON Output Files
🛠 Technology Stack
Backend
Technology	Purpose
Python	Core Development
Pydantic	Data Validation
JSON	Runtime Configuration
CSV	Structured Input
Logging	Pipeline Monitoring
Pytest	Automated Testing
Development Tools
Technology	Purpose
Git	Version Control
GitHub	Repository Hosting
VS Code	Development IDE
📂 Project Structure
CandidateSync/
│
├── config/
│   ├── default_config.json
│   └── custom_minimal_config.json
│
├── docs/
│   └── SourabiR_Email_Eightfold.pdf
│
├── input/
│   ├── sample_candidates.csv
│   └── resume.txt
│
├── output/
│   ├── candidate_profile.json
│   ├── candidate_profiles.json
│   ├── statistics.json
│   ├── duplicates.json
│   ├── conflict_report.json
│   └── log.txt
│
├── src/
│
├── tests/
│
├── README.md
├── requirements.txt
└── .gitignore
🚀 Getting Started
Clone Repository
git clone https://github.com/Sourabi-R/CandidateSync.git

cd CandidateSync
Create Virtual Environment
python -m venv .venv
Windows
.venv\Scripts\activate
macOS/Linux
source .venv/bin/activate
Install Dependencies
pip install -r requirements.txt
▶️ Run the Pipeline
Default Schema
python -m src.cli.main \
--csv input/sample_candidates.csv \
--resume input/resume.txt \
--config config/default_config.json
Custom Runtime Output
python -m src.cli.main \
--csv input/sample_candidates.csv \
--resume input/resume.txt \
--config config/custom_minimal_config.json
🧪 Run Tests
pytest

Expected Output

========================

25 passed

========================
⚠️ Edge Cases Handled
Missing Resume
Missing CSV
Duplicate Candidates
Invalid Phone Numbers
Missing Emails
Conflicting Candidate Information
Empty Input Files
Malformed Runtime Configuration
🔮 Future Enhancements
ATS JSON Integration
GitHub Profile Parsing
LinkedIn Profile Parsing
PDF Resume Parsing
DOCX Resume Support
REST API Interface
Web Dashboard
AI-Based Entity Resolution
Semantic Skill Matching
Cloud Deployment
👩‍💻 Author

Sourabi R

B.Tech – Artificial Intelligence & Data Science

CandidateSync — Multi-Source Candidate Data Transformer 🚀
