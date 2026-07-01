import logging
import sys
from pathlib import Path

from src.config.constants import DEFAULT_LOG_LEVEL, DEFAULT_OUTPUT_DIR, LOG_FILE


class Logger:
    """Configure application logging to console and file."""

    @staticmethod
    def setup() -> logging.Logger:
        output_path = Path(DEFAULT_OUTPUT_DIR)
        output_path.mkdir(parents=True, exist_ok=True)

        log_path = output_path / LOG_FILE
        logging.basicConfig(
            level=getattr(logging, DEFAULT_LOG_LEVEL, logging.INFO),
            format="INFO %(message)s",
            handlers=[
                logging.FileHandler(log_path, encoding="utf-8", mode="w"),
                logging.StreamHandler(sys.stdout),
            ],
            force=True,
        )
        return logging.getLogger("CandidateSync")
