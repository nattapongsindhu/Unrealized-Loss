"""
fetch_btc.py
Pull Bitcoin daily close prices from Yahoo Finance (yfinance).
No API key required. Saves to data/btc_prices.csv
"""

import yfinance as yf
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
BTC_FILE  = DATA_DIR / "btc_prices.csv"

START_DATE = "2021-10-01"


def fetch_btc(start: str = START_DATE) -> pd.DataFrame:
    print(f"Fetching BTC-USD from Yahoo Finance (from {start})...")
    ticker = yf.download("BTC-USD", start=start, progress=False, auto_adjust=True)
    df = ticker[["Close"]].reset_index()
    df.columns = ["date", "price"]
    df["date"]  = pd.to_datetime(df["date"]).dt.date
    df["price"] = df["price"].round(2)
    df = df.dropna().sort_values("date").reset_index(drop=True)
    return df


def save_btc(df: pd.DataFrame):
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(BTC_FILE, index=False)
    print(f"Saved {len(df)} rows → {BTC_FILE}")


if __name__ == "__main__":
    df = fetch_btc()
    save_btc(df)
    print(df.tail(3).to_string(index=False))
