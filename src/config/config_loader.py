import json
from pathlib import Path
from typing import Any

from src.config.constants import DEFAULT_CONFIG_PATH


class ConfigLoader:
    @staticmethod
    def load(config_path: str | None = None) -> dict[str, Any]:
        """Load the pipeline configuration from a JSON file."""
        path = Path(config_path or DEFAULT_CONFIG_PATH)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(f"Config parsing failed: {error}") from error
