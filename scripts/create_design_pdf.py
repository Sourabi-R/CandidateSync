from pathlib import Path
from datetime import datetime
import textwrap

pdf_path = Path('docs/SourabiR_yourmail_Eightfold.pdf')
pdf_text = f"""CandidateSync Design Summary

Author: Sourabi R
Email: yourmail@example.com
Date: {datetime.utcnow().date()}

Project Overview:
CandidateSync ingests structured recruiter CSV data and unstructured resume content, normalizes values, merges into a canonical profile, adds confidence and provenance, validates output, and projects JSON based on runtime config.

Architecture:
- CSV Parser
- Resume Parser
- Canonical Mapper
- Merge Engine
- Confidence Engine
- Projection Layer
- Output Validator
- CLI + Logging + Reports

Merge Strategy:
- CSV is the primary source for structured fields.
- Resume enriches contact data and skills.
- Conflicts are recorded in conflict_report.json for traceability.

Confidence:
- Overall confidence is computed from merged profile heuristics.
- Confidence is included when enabled by config.

Projection:
- Config controls field selection, confidence, and provenance.
- Minimal config hides metadata; default config includes full traceability.

Validation:
- Required fields are enforced during output validation.
- Missing required projected fields cause a validation error.

Edge Cases:
- Missing resume file logs an error and continues safely.
- Duplicate emails and phones are normalized and deduplicated.
- Phone numbers are normalized to E.164.
"""

lines = textwrap.wrap(pdf_text, width=90)

content = 'BT /F1 10 Tf 50 760 Td ({text}) Tj ET'.format(text=lines[0].replace('(', '\(').replace(')', '\)'))
text_objects = []
for i, line in enumerate(lines):
    y = 760 - i * 14
    escaped = line.replace('(', '\(').replace(')', '\)').replace('\\', '\\\\')
    text_objects.append(f'BT /F1 10 Tf 50 {y} Td ({escaped}) Tj ET')

page_content = '\n'.join(text_objects)

# Build minimal PDF
objects = []
objects.append('1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj')
objects.append('2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj')
objects.append('3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj')
objects.append(f'4 0 obj << /Length {len(page_content.encode("latin1"))} >> stream\n{page_content}\nendstream endobj')
objects.append('5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj')

body = '%PDF-1.4\n\n'
offsets = []
current = len(body.encode('latin1'))
for obj in objects:
    offsets.append(current)
    body += obj + '\n\n'
    current = len(body.encode('latin1'))

xref_start = len(body.encode('latin1'))
body += 'xref\n0 {count}\n'.format(count=len(objects)+1)
body += '0000000000 65535 f \n'
for offset in offsets:
    body += f'{offset:010d} 00000 n \n'
body += f'trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref {xref_start}\n%%EOF\n'

pdf_path.write_bytes(body.encode('latin1'))
print(f'Created {pdf_path}')
