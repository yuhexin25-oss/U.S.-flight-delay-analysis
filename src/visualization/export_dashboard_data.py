"""Export processed CSV metrics as browser-friendly JSON."""

from __future__ import annotations

import json

import pandas as pd

from src.config import PROCESSED_DATA_DIR, PROJECT_ROOT


def main() -> None:
    frame = pd.read_csv(PROCESSED_DATA_DIR / "airport_metrics.csv").fillna("")
    output = PROJECT_ROOT / "web" / "data" / "airport_metrics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(frame.to_dict(orient="records"), indent=2), encoding="utf-8")
    print(f"Exported {len(frame)} airport records to {output}")


if __name__ == "__main__":
    main()

