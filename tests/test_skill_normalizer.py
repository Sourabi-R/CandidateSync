from src.normalizer.skill_normalizer import normalize_skills


def test_skill_normalizer_canonicalizes_and_sorts():
    skills = ["python", "PYTHON", "js", "Java Script", "aws", "docker"]
    normalized = normalize_skills(skills)

    assert normalized == ["AWS", "Docker", "JavaScript", "Python"]


def test_skill_normalizer_removes_duplicates():
    skills = ["js", "javascript", "JavaScript"]
    normalized = normalize_skills(skills)

    assert normalized == ["JavaScript"]
