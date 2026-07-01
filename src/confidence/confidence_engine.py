from typing import Any

from src.config.constants import DEFAULT_CONFIDENCE_WEIGHTS, DEFAULT_SOURCE_RELIABILITY


class ConfidenceEngine:
    """Calculate a confidence score based on profile completeness and source reliability."""

    @staticmethod
    def calculate(profile: Any, conflict_count: int = 0) -> Any:
        weights = DEFAULT_CONFIDENCE_WEIGHTS
        score = 0.0
        max_score = 1.0

        completeness = 0
        fields = [
            bool(profile.full_name),
            bool(profile.emails),
            bool(profile.phones),
            bool(profile.skills),
            bool(profile.experience),
            bool(profile.education),
            bool(profile.provenance),
        ]
        completeness = sum(int(value) for value in fields)
        score += (completeness / len(fields)) * weights["field_presence"]

        source_reliability = 0.0
        if profile.provenance:
            for provenance in profile.provenance:
                source = getattr(provenance, "source", None) if provenance is not None else None
                if source is None and isinstance(provenance, dict):
                    source = provenance.get("source")
                source_reliability += DEFAULT_SOURCE_RELIABILITY.get(source, 0.5)
            source_reliability = min(source_reliability / len(profile.provenance), 1.0)
        score += source_reliability * weights["source_reliability"]

        conflict_penalty = min(conflict_count * 0.05, 1.0)
        score -= conflict_penalty * weights["conflict_penalty"]

        profile.overall_confidence = round(max(0.0, min(score, max_score)), 2)
        return profile
