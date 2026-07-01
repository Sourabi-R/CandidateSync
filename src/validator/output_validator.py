from typing import Any


class OutputValidator:
    """Validate projected output against configuration requirements."""

    @staticmethod
    def validate(output: dict[str, Any], config: dict[str, Any]) -> bool:
        for field in config.get("fields", []):
            if field.get("required"):
                target = field["path"]
                if output.get(target) is None:
                    raise ValueError(f"Missing required field: {target}")
        return True
