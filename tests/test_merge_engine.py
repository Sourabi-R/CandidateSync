from src.mapper.canonical_mapper import CanonicalMapper
from src.merger.merge_engine import MergeEngine


def test_merge_engine_deduplicates_phone_numbers():
    csv_profile = CanonicalMapper.map_csv(
        {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+14155550100",
            "years_experience": 8,
            "current_company": "Acme",
            "current_title": "Engineer",
        }
    )
    resume_data = {"phone": "+1-415-555-0100", "skills": ["Python"]}

    merged_profile, _ = MergeEngine.merge(csv_profile, resume_data)

    assert merged_profile.phones == ["+14155550100"]
