from src.confidence.confidence_engine import ConfidenceEngine
from src.mapper.canonical_mapper import CanonicalMapper


def test_confidence_engine_calculates_score():
    profile = CanonicalMapper.map_csv(
        {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "+14155550100",
            "years_experience": 3,
            "current_company": "Acme",
            "current_title": "Engineer",
        }
    )
    profile.provenance.append(
        {
            "field": "full_name",
            "source": "csv",
            "method": "csv_mapping",
        }
    )

    updated_profile = ConfidenceEngine.calculate(profile, conflict_count=0)
    assert updated_profile.overall_confidence is not None
    assert 0.0 <= updated_profile.overall_confidence <= 1.0
