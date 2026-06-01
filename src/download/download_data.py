"""Download source extracts or create a lightweight local demo dataset."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import urllib.request
from pathlib import Path

from src.config import PRIORITY_YEARS, RAW_DATA_DIR, SUPPORTED_YEARS, ensure_directories

OPENFLIGHTS_AIRPORTS_URL = (
    "https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat"
)
BTS_PREZIP_ROOT = "https://www.transtats.bts.gov/PREZIP"

SAMPLE_FLIGHTS = [
    ("2025-01-05", "DL", "ATL", "JFK", 8, 12, 0, 0, 3, 0, 5, 0, 4),
    ("2025-01-05", "AA", "DFW", "LAX", 18, 22, 0, 0, 8, 0, 10, 0, 4),
    ("2025-01-06", "UA", "ORD", "SFO", 31, 38, 0, 0, 4, 9, 12, 0, 13),
    ("2025-01-06", "B6", "JFK", "BTV", 52, 61, 0, 0, 5, 41, 8, 0, 7),
    ("2025-01-07", "AA", "CLT", "ROA", -2, 3, 0, 0, 0, 0, 0, 0, 3),
    ("2025-01-07", "UA", "DEN", "SFO", 14, 19, 0, 0, 2, 5, 6, 0, 6),
    ("2025-01-08", "DL", "ATL", "AVL", 0, -4, 0, 0, 0, 0, 0, 0, 0),
    ("2025-01-08", "AA", "DFW", "FAT", 44, 47, 0, 0, 13, 0, 18, 0, 16),
    ("2025-01-09", "UA", "SFO", "LAX", 27, 34, 0, 0, 7, 0, 9, 0, 18),
    ("2025-01-09", "DL", "JFK", "CHO", 0, 0, 1, 0, 0, 0, 0, 0, 0),
    ("2025-02-01", "AA", "LAX", "DFW", 11, 16, 0, 0, 6, 0, 5, 0, 5),
    ("2025-02-02", "UA", "ORD", "DEN", 63, 70, 0, 0, 15, 22, 18, 0, 15),
]

SAMPLE_AIRPORTS = [
    ("ATL", "Hartsfield-Jackson Atlanta International", "Atlanta", "GA", 33.6407, -84.4277, "Large Hub", 5),
    ("ORD", "Chicago O'Hare International", "Chicago", "IL", 41.9742, -87.9073, "Large Hub", 8),
    ("DFW", "Dallas Fort Worth International", "Dallas", "TX", 32.8998, -97.0403, "Large Hub", 7),
    ("DEN", "Denver International", "Denver", "CO", 39.8561, -104.6737, "Large Hub", 6),
    ("LAX", "Los Angeles International", "Los Angeles", "CA", 33.9416, -118.4085, "Large Hub", 4),
    ("SFO", "San Francisco International", "San Francisco", "CA", 37.6213, -122.3790, "Large Hub", 4),
    ("CLT", "Charlotte Douglas International", "Charlotte", "NC", 35.2140, -80.9431, "Large Hub", 4),
    ("JFK", "John F. Kennedy International", "New York", "NY", 40.6413, -73.7781, "Large Hub", 4),
    ("ROA", "Roanoke-Blacksburg Regional", "Roanoke", "VA", 37.3255, -79.9754, "Regional", 2),
    ("BTV", "Patrick Leahy Burlington International", "Burlington", "VT", 44.4719, -73.1533, "Regional", 2),
    ("AVL", "Asheville Regional", "Asheville", "NC", 35.4362, -82.5418, "Regional", 1),
    ("FAT", "Fresno Yosemite International", "Fresno", "CA", 36.7762, -119.7181, "Regional", 2),
    ("CHO", "Charlottesville-Albemarle", "Charlottesville", "VA", 38.1386, -78.4529, "Regional", 1),
]


def _write_csv(path: Path, header: tuple[str, ...], rows: list[tuple[object, ...]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def write_sample_data() -> None:
    """Write compact source-shaped files for development and CI."""
    ensure_directories()
    _write_csv(
        RAW_DATA_DIR / "flights_sample.csv",
        ("flight_date", "carrier", "origin", "destination", "departure_delay",
         "arrival_delay", "cancelled", "diverted", "carrier_delay", "weather_delay",
         "nas_delay", "security_delay", "late_aircraft_delay"),
        SAMPLE_FLIGHTS,
    )
    _write_csv(
        RAW_DATA_DIR / "airports_sample.csv",
        ("iata", "airport_name", "city", "state", "latitude", "longitude",
         "hub_classification", "runway_count"),
        SAMPLE_AIRPORTS,
    )
    manifest = {"mode": "sample", "flight_rows": len(SAMPLE_FLIGHTS), "airport_rows": len(SAMPLE_AIRPORTS)}
    (RAW_DATA_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote sample extracts to {RAW_DATA_DIR}")


def download_file(url: str, destination: Path) -> None:
    """Download a URL atomically enough for repeatable local ingestion."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)


def bts_monthly_url(year: int, month: int) -> str:
    """Return the official TranStats prezipped monthly on-time archive URL."""
    filename = f"On_Time_Reporting_Carrier_On_Time_Performance_1987_present_{year}_{month}.zip"
    return f"{BTS_PREZIP_ROOT}/{filename}"


def download_source_data(years: list[int], months: list[int], skip_bts: bool = False) -> None:
    """Download OpenFlights and selected official BTS monthly archives."""
    ensure_directories()
    target = RAW_DATA_DIR / "openflights_airports.dat"
    download_file(OPENFLIGHTS_AIRPORTS_URL, target)
    print(f"Downloaded OpenFlights airports to {target}")
    if not skip_bts:
        for year in years:
            for month in months:
                url = bts_monthly_url(year, month)
                archive = RAW_DATA_DIR / "bts" / f"{year}" / Path(url).name
                download_file(url, archive)
                print(f"Downloaded BTS {year}-{month:02d} to {archive}")
    print("FAA airport CSVs and NOAA observations can be added under data/raw/ for enrichment.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", action="store_true", help="write small offline demo extracts")
    parser.add_argument("--years", nargs="+", type=int, default=list(PRIORITY_YEARS))
    parser.add_argument("--months", nargs="+", type=int, default=list(range(1, 13)))
    parser.add_argument("--skip-bts", action="store_true", help="download reference data only")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    unsupported = sorted(set(args.years) - set(SUPPORTED_YEARS))
    if unsupported:
        raise SystemExit(f"Unsupported years: {unsupported}. Choose from {SUPPORTED_YEARS}.")
    invalid_months = sorted(set(args.months) - set(range(1, 13)))
    if invalid_months:
        raise SystemExit(f"Invalid months: {invalid_months}. Choose from 1-12.")
    if args.sample:
        write_sample_data()
    else:
        download_source_data(args.years, args.months, args.skip_bts)


if __name__ == "__main__":
    main()
