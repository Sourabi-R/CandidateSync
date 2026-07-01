from pathlib import Path
from typing import Any

import pandas as pd
from pandas.errors import EmptyDataError


class CSVParser:
    """Parser for recruiter CSV files."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def parse(self) -> list[dict[str, Any]]:
        """Read recruiter CSV and return a list of records."""
        path = Path(self.file_path)
        if not path.exists():
            raise FileNotFoundError(f"CSV not found: {path}")

        try:
            dataframe = pd.read_csv(path)
        except EmptyDataError:
            return []
        except Exception as error:
            raise ValueError(f"CSV parsing failed: {error}") from error

        if dataframe.empty:
            return []

        return dataframe.to_dict(orient="records")
