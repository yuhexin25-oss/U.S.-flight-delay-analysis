"""Validate and standardize raw flight and airport extracts."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR, ensure_directories

FLIGHT_COLUMNS = {
    "flight_date", "carrier", "origin", "destination", "departure_delay",
    "arrival_delay", "cancelled", "diverted", "carrier_delay", "weather_delay",
    "nas_delay", "security_delay", "late_aircraft_delay",
}
AIRPORT_COLUMNS = {
    "iata", "airport_name", "city", "state", "latitude", "longitude",
    "hub_classification", "runway_count",
}


def _require_columns(frame: pd.DataFrame, required: set[str], label: str) -> None:
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{label} extract is missing required columns: {sorted(missing)}")


def clean_flights(source: Path, destination: Path) -> pd.DataFrame:
    frame = pd.read_csv(source)
    frame.columns = frame.columns.str.strip().str.lower()
    _require_columns(frame, FLIGHT_COLUMNS, "flight")
    frame["flight_date"] = pd.to_datetime(frame["flight_date"], errors="raise")
    for column in ("carrier", "origin", "destination"):
        frame[column] = frame[column].astype("string").str.strip().str.upper()
    numeric = FLIGHT_COLUMNS - {"flight_date", "carrier", "origin", "destination"}
    frame[list(numeric)] = frame[list(numeric)].apply(pd.to_numeric, errors="coerce").fillna(0)
    frame["cancelled"] = frame["cancelled"].astype(bool)
    frame["diverted"] = frame["diverted"].astype(bool)
    frame.to_csv(destination, index=False)
    return frame


def clean_airports(source: Path, destination: Path) -> pd.DataFrame:
    frame = pd.read_csv(source)
    frame.columns = frame.columns.str.strip().str.lower()
    _require_columns(frame, AIRPORT_COLUMNS, "airport")
    frame["iata"] = frame["iata"].astype("string").str.strip().str.upper()
    frame = frame.dropna(subset=["iata", "latitude", "longitude"]).drop_duplicates("iata")
    frame.to_csv(destination, index=False)
    return frame


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", action="store_true", help="clean bundled demo-shaped extracts")
    args = parser.parse_args()
    ensure_directories()
    suffix = "_sample" if args.sample else ""
    flights = clean_flights(RAW_DATA_DIR / f"flights{suffix}.csv", PROCESSED_DATA_DIR / "flights.csv")
    airports = clean_airports(RAW_DATA_DIR / f"airports{suffix}.csv", PROCESSED_DATA_DIR / "airports.csv")
    print(f"Cleaned {len(flights)} flights and {len(airports)} airports.")


if __name__ == "__main__":
    main()

