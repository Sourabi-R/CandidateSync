from src.projection.projector import Projector
from src.mapper.canonical_mapper import CanonicalMapper


def test_projector_uses_runtime_config(tmp_path):
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

    config_path = tmp_path / "config.json"
    config_path.write_text(
        '{"fields": [{"path": "candidate_name", "from": "full_name"}], "include_confidence": false, "include_provenance": false, "on_missing": "null"}'
    )

    output = Projector.project(profile, str(config_path))

    assert output["candidate_name"] == "Jane Doe"
