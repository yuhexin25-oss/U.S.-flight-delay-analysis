"""Create enriched flight records and dashboard-ready aggregate tables."""

from __future__ import annotations

import argparse

import pandas as pd

from src.config import PROCESSED_DATA_DIR, ensure_directories


def build_analytical_tables() -> None:
    ensure_directories()
    flights = pd.read_csv(PROCESSED_DATA_DIR / "flights.csv", parse_dates=["flight_date"])
    airports = pd.read_csv(PROCESSED_DATA_DIR / "airports.csv")
    origin = airports.add_prefix("origin_")
    enriched = flights.merge(origin, left_on="origin", right_on="origin_iata", how="left")
    enriched.to_csv(PROCESSED_DATA_DIR / "flights_enriched.csv", index=False)

    metrics = (
        enriched.groupby(["origin", "origin_airport_name", "origin_city", "origin_state",
                          "origin_latitude", "origin_longitude", "origin_hub_classification"],
                         dropna=False)
        .agg(
            total_flights=("origin", "size"),
            average_delay=("arrival_delay", "mean"),
            median_delay=("arrival_delay", "median"),
            cancellation_rate=("cancelled", "mean"),
        )
        .reset_index()
        .rename(columns=lambda value: value.removeprefix("origin_"))
    )
    metrics["cancellation_rate"] = metrics["cancellation_rate"] * 100
    metrics.to_csv(PROCESSED_DATA_DIR / "airport_metrics.csv", index=False)
    metrics.to_csv(PROCESSED_DATA_DIR / "sample_airport_metrics.csv", index=False)

    routes = (
        enriched.groupby(["origin", "destination"])
        .agg(total_flights=("origin", "size"), average_delay=("arrival_delay", "mean"))
        .reset_index()
    )
    routes.to_csv(PROCESSED_DATA_DIR / "route_metrics.csv", index=False)
    print(f"Built analytical tables for {len(metrics)} origin airports and {len(routes)} routes.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", action="store_true", help="accepted for Makefile symmetry")
    parser.parse_args()
    build_analytical_tables()


if __name__ == "__main__":
    main()

