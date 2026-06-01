"""Shared paths and supported date ranges for the analytics pipeline."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "flight_delays.duckdb"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"

SUPPORTED_YEARS = tuple(range(2019, 2026))
PRIORITY_YEARS = (2023, 2024, 2025)


def ensure_directories() -> None:
    """Create generated-data directories when running from a fresh clone."""
    for path in (RAW_DATA_DIR, PROCESSED_DATA_DIR, DATABASE_DIR):
        path.mkdir(parents=True, exist_ok=True)

