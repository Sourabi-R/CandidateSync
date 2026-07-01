import pytest

from src.validator.output_validator import OutputValidator


def test_output_validator_passes_when_required_fields_present():
    output = {"name": "Jane", "email": "jane@example.com"}
    config = {"fields": [{"path": "name", "required": True}, {"path": "email", "required": True}]}

    assert OutputValidator.validate(output, config) is True


def test_output_validator_raises_when_required_field_missing():
    output = {"name": "Jane"}
    config = {"fields": [{"path": "name", "required": True}, {"path": "email", "required": True}]}

    with pytest.raises(ValueError, match="Missing required field: email"):
        OutputValidator.validate(output, config)
