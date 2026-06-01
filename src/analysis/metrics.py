"""Reusable airport, route, and delay-cause calculations."""

from __future__ import annotations

import pandas as pd

DELAY_CAUSES = [
    "carrier_delay", "weather_delay", "nas_delay", "security_delay", "late_aircraft_delay",
]


def airport_performance(flights: pd.DataFrame) -> pd.DataFrame:
    """Summarize operational performance by origin airport."""
    metrics = flights.groupby("origin").agg(
        total_flights=("origin", "size"),
        average_departure_delay=("departure_delay", "mean"),
        average_arrival_delay=("arrival_delay", "mean"),
        median_arrival_delay=("arrival_delay", "median"),
        cancellation_rate=("cancelled", "mean"),
    )
    return metrics.sort_values("average_arrival_delay", ascending=False)


def delay_cause_breakdown(flights: pd.DataFrame) -> pd.Series:
    """Return the share of reported delay minutes attributable to each cause."""
    totals = flights[DELAY_CAUSES].sum()
    return (totals / totals.sum()).sort_values(ascending=False)

