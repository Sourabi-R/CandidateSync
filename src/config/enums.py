from enum import Enum


class DataSource(str, Enum):
    CSV = "csv"
    RESUME = "resume"
