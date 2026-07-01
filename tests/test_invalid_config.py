import pytest
from src.config.config_loader import ConfigLoader


def test_invalid_config_raises_value_error(tmp_path):
    config_file = tmp_path / "invalid_config.json"
    config_file.write_text("{ invalid json }")

    with pytest.raises(ValueError):
        ConfigLoader.load(str(config_file))


def test_missing_config_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        ConfigLoader.load(str(tmp_path / "missing.json"))
