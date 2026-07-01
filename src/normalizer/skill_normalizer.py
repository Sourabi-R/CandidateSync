"""Skill normalization utilities."""

import re

SKILL_CANONICAL_MAP = {
    "py": "Python",
    "python": "Python",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "java script": "JavaScript",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "node": "Node.js",
    "sql": "SQL",
    "aws": "AWS",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "react": "React",
    "c++": "C++",
    "c#": "C#",
    "html": "HTML",
    "css": "CSS",
}


def normalize_skills(skills: list[str]) -> list[str]:
    """Normalize a list of skill strings into canonical titles.

    This removes duplicates, maps common aliases, and sorts results.
    """
    normalized: set[str] = set()
    for skill in skills:
        if not skill or not skill.strip():
            continue

        key = re.sub(r"[\.\s\-]+", "", skill.strip().lower())
        canonical = SKILL_CANONICAL_MAP.get(key)
        if not canonical:
            canonical = skill.strip().title()
        normalized.add(canonical)

    return sorted(normalized, key=str.casefold)
