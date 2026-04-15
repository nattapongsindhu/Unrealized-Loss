"""
fetch_stamp.py
Load USPS stamp price history and forward-fill to daily series.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
STAMP_FILE = DATA_DIR / "stamp_prices.csv"


def load_stamp(start: str = "2021-10-01", end: str = None) -> pd.DataFrame:
    df = pd.read_csv(STAMP_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    end_date = pd.Timestamp(end) if end else pd.Timestamp.today()
    date_range = pd.date_range(start=start, end=end_date, freq="D")

    df = df.set_index("date").reindex(date_range).ffill().bfill().reset_index()
    df.columns = ["date", "price_cents"]
    df["date"] = df["date"].dt.date
    return df


if __name__ == "__main__":
    df = load_stamp()
    print(df.tail(5).to_string(index=False))
    print(f"\nTotal rows: {len(df)}")
