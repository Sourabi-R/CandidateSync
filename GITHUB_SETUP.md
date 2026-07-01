# GitHub Setup Guide

## How to Create & Push Your Repository

### Step 1: Create a New Repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. **Repository name**: `CandidateSync`
3. **Description**: 
   ```
   A configurable multi-source candidate data transformer that consolidates structured and unstructured candidate information into a canonical profile with provenance, confidence scoring, normalization, and schema validation.
   ```
4. **Visibility**: Public
5. **Initialize with**: None (we'll push existing files)
6. Click **Create repository**

---

### Step 2: Initialize Git Locally

Navigate to your CandidateSync folder and run:

```bash
cd /Users/shivnavin/CandidateSync

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Project planning and structure

- Created folder structure (docs, input, output, config, src, tests, assets)
- Added project documentation (README, PROJECT_SCOPE, DESIGN_NOTES)
- Defined canonical schema and normalization strategy
- Configured runtime output projection
- Created sample input data and configurations
- Identified edge cases and merge strategy
- Set up requirements.txt with tech stack"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/CandidateSync.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

### Step 3: Verify

Visit: `https://github.com/YOUR_USERNAME/CandidateSync`

You should see all your files uploaded.

---

## Next Commits

After each phase:

### Phase 2 (Implementation)
```bash
git add .
git commit -m "Phase 2: Implement core pipeline

- Implemented CSV and PDF parsers
- Built field extractors with regex patterns
- Added normalization (phones, dates, countries, skills)
- Implemented merge & deduplication logic
- Built confidence scoring engine
- Added runtime config projection
- Implemented schema validation
- Created CLI interface with typer"
```

### Phase 3 (Testing)
```bash
git add .
git commit -m "Phase 3: Add tests and edge case handling

- Added unit tests for all modules
- Tested edge cases (malformed data, conflicts, etc.)
- Added integration tests end-to-end
- Generated sample outputs
- Updated documentation"
```

### Phase 4 (Demo)
```bash
git add .
git commit -m "Phase 4: Add demo and final documentation

- Added demo video link to README
- Updated design PDF reference
- Added architecture diagrams
- Updated README with run instructions
- Added design decisions documentation"
```

---

## .gitignore Notes

Your `.gitignore` already excludes:
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files
- `.venv/` - Virtual environment
- `.pytest_cache/` - Test cache
- `output/*.json` - Generated files (keep structure with `.gitkeep`)

---

## Tips

- **Commit often**: After each feature, commit with clear messages
- **Use branches** for experimental features: `git checkout -b feature/my-feature`
- **Keep README updated** as you progress
- **Add tags** for major milestones: `git tag -a v1.0 -m "Phase 1 complete"`

---

## Reference: Typical Repository Contents

By the end, your repository should have:

```
CandidateSync/
├── .github/
│   └── workflows/             (Optional: CI/CD)
├── docs/
│   ├── Eightfold_Design.pdf   (REQUIRED)
│   ├── ARCHITECTURE.md
│   └── ...
├── input/
│   ├── sample_candidates.csv  (REQUIRED)
│   └── sample_resume.pdf      (Optional)
├── output/
│   ├── default.json           (REQUIRED - sample output)
│   └── custom_minimal.json    (REQUIRED - custom config output)
├── config/
│   ├── default_config.json
│   └── custom_minimal_config.json
├── src/                       (REQUIRED - implementation)
│   ├── __init__.py
│   ├── main.py
│   ├── cli/
│   ├── parsers/
│   ├── extractors/
│   ├── normalizers/
│   ├── merger/
│   ├── confidence/
│   ├── projector/
│   └── validator/
├── tests/                     (REQUIRED - tests)
│   ├── test_parsers.py
│   ├── test_extractors.py
│   ├── test_normalizers.py
│   ├── test_merge.py
│   └── test_edge_cases.py
├── assets/                    (Optional: images, diagrams)
├── README.md                  (REQUIRED)
├── requirements.txt           (REQUIRED)
├── .gitignore                 ✅ Done
└── STEP1_CHECKLIST.md         (Can delete or archive after Phase 1)
```

---

## Questions?

- For GitHub help: [github.com/git-tips](https://github.com/git-tips/tips)
- For git workflow: [atlassian.com/git](https://www.atlassian.com/git)

