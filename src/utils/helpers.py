"""General helper utilities."""


def safe_get(data: dict, key: str, default=None):
    """Safely retrieve a value from a dictionary."""
    return data.get(key, default)
