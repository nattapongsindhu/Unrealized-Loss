"""
calculate_index.py
Merge all three series, normalize to 100 at start date, compute metrics.
"""

import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from fetch_stamp import load_stamp
from generate_heart import generate_heart

DATA_DIR = Path(__file__).parent.parent / "data"
BTC_FILE = DATA_DIR / "btc_prices.csv"

START = "2021-10-01"
END = "2024-08-23"


def build_index() -> pd.DataFrame:
    # --- Stamp ---
    stamp = load_stamp(start=START)
    stamp["date"] = pd.to_datetime(stamp["date"])

    # --- BTC ---
    btc = pd.read_csv(BTC_FILE, parse_dates=["date"])

    # --- Heart ---
    heart = generate_heart()
    heart["date"] = pd.to_datetime(heart["date"])

    # Merge on date
    df = stamp.merge(btc, on="date", how="inner").merge(heart, on="date", how="inner")

    df = df.sort_values("date").reset_index(drop=True)

    # Normalize to 100 at first row
    df["stamp_idx"] = df["price_cents"] / df["price_cents"].iloc[0] * 100
    df["btc_idx"] = df["price"] / df["price"].iloc[0] * 100
    df["heart_idx"] = df["heart_index"]

    return df[["date", "stamp_idx", "btc_idx", "heart_idx"]]


def metrics(series: pd.Series, name: str) -> dict:
    daily_ret = series.pct_change().dropna()
    total_ret = (series.iloc[-1] / series.iloc[0] - 1) * 100
    roll_max = series.cummax()
    drawdown = (series - roll_max) / roll_max
    max_dd = drawdown.min() * 100
    vol = daily_ret.std() * 100

    return {
        "asset": name,
        "start_value": round(series.iloc[0], 2),
        "end_value": round(series.iloc[-1], 2),
        "total_return": round(total_ret, 2),
        "max_drawdown": round(max_dd, 2),
        "volatility": round(vol, 4),
    }


if __name__ == "__main__":
    df = build_index()
    print(f"Date range: {df['date'].iloc[0].date()} → {df['date'].iloc[-1].date()}")
    print(f"Rows: {len(df)}\n")

    for col, name in [
        ("stamp_idx", "Stamp"),
        ("btc_idx", "Bitcoin"),
        ("heart_idx", "Heart"),
    ]:
        m = metrics(df[col], name)
        print(f"[{name}]")
        for k, v in m.items():
            print(f"  {k}: {v}")
        print()
