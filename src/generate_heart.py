"""
generate_heart.py
Generate the Heart Index — starts at 100, decays after relationship ends.
Formula: 100 * e^(-0.003 * days_since_end)
Half-life: ~231 days. Floor: 0. No recovery.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).parent.parent / "data"
HEART_FILE = DATA_DIR / "heart_index.csv"

RELATIONSHIP_START = date(2021, 10, 1)
RELATIONSHIP_END   = date(2024, 8, 23)
DECAY_RATE         = 0.003


def generate_heart(start: date = RELATIONSHIP_START,
                   end: date   = RELATIONSHIP_END,
                   until: date = None) -> pd.DataFrame:

    until = until or date.today()
    date_range = pd.date_range(start=str(start), end=str(until), freq="D")
    days = np.arange(len(date_range))

    end_idx = (pd.Timestamp(end) - pd.Timestamp(start)).days

    values = np.where(
        days <= end_idx,
        100.0,
        100.0 * np.exp(-DECAY_RATE * (days - end_idx))
    )

    df = pd.DataFrame({"date": date_range.date, "heart_index": np.round(values, 4)})
    return df


def save_heart(df: pd.DataFrame):
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(HEART_FILE, index=False)
    print(f"Saved {len(df)} rows → {HEART_FILE}")


if __name__ == "__main__":
    df = generate_heart()
    save_heart(df)
    print(df[df["date"] >= RELATIONSHIP_END].head(10).to_string(index=False))
