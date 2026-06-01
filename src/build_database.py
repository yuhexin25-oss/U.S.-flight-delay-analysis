"""Load processed analytical data into DuckDB."""

from __future__ import annotations

import duckdb

from src.config import DATABASE_PATH, PROCESSED_DATA_DIR, SCHEMA_PATH, ensure_directories


def build_database() -> None:
    ensure_directories()
    with duckdb.connect(str(DATABASE_PATH)) as connection:
        connection.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.execute("DELETE FROM airports")
        connection.execute("DELETE FROM flights")
        connection.execute(
            "INSERT INTO airports SELECT * FROM read_csv_auto(?)",
            [str(PROCESSED_DATA_DIR / "airports.csv")],
        )
        connection.execute(
            "INSERT INTO flights SELECT * FROM read_csv_auto(?)",
            [str(PROCESSED_DATA_DIR / "flights.csv")],
        )
        flight_count = connection.execute("SELECT COUNT(*) FROM flights").fetchone()[0]
    print(f"Loaded {flight_count} flights into {DATABASE_PATH}")


if __name__ == "__main__":
    build_database()

