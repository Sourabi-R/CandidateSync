from __future__ import annotations

from pathlib import Path
from typing import Any

from src.config.config_loader import ConfigLoader


def _resolve_source(profile_dict: dict[str, Any], source: str) -> Any:
    """Resolve a source expression to a value within the profile dictionary."""
    if source == "confidence":
        return {"overall_confidence": profile_dict.get("overall_confidence")}

    if "[" in source or "." in source:
        current: Any = profile_dict
        for part in source.replace("]", "").split("."):
            if "[" in part:
                key, index = part.split("[")
                current = current.get(key) if isinstance(current, dict) else None
                if current is None:
                    return None
                try:
                    current = current[int(index)]
                except (IndexError, ValueError, TypeError):
                    return None
            else:
                if isinstance(current, dict):
                    current = current.get(part)
                else:
                    return None
            if current is None:
                return None
        return current

    return profile_dict.get(source)


class Projector:
    """Project a canonical profile into configured JSON output."""

    @staticmethod
    def project(profile: Any, config: str | Path | dict[str, Any]) -> dict[str, Any]:
        if isinstance(config, (str, Path)):
            config = ConfigLoader.load(str(config))

        profile_dict = profile.model_dump() if hasattr(profile, "model_dump") else dict(profile)
        output: dict[str, Any] = {}
        on_missing = config.get("on_missing", "null")

        for field in config.get("fields", []):
            source = field["from"]
            target = field["path"]
            value = _resolve_source(profile_dict, source)
            output[target] = value if value is not None else None if on_missing == "null" else value

        if config.get("include_confidence") and "confidence" not in output:
            output["confidence"] = {"overall_confidence": profile_dict.get("overall_confidence")}

        if config.get("include_provenance") and "provenance" not in output:
            output["provenance"] = profile_dict.get("provenance")

        return output
