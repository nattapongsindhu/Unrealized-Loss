"""
fetch_btc.py
Pull Bitcoin daily close prices from Yahoo Finance (yfinance).
Includes error handling and logging — if API fails, logs warning instead of crashing.
"""

import yfinance as yf
import pandas as pd
import logging
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
BTC_FILE = DATA_DIR / "btc_prices.csv"
START_DATE = "2021-10-01"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def fetch_btc(start: str = START_DATE) -> pd.DataFrame | None:
    try:
        log.info(f"Fetching BTC-USD from Yahoo Finance (from {start})...")
        ticker = yf.download("BTC-USD", start=start, progress=False, auto_adjust=True)

        if ticker.empty:
            log.warning("Yahoo Finance returned empty data — skipping update.")
            return None

        df = ticker[["Close"]].reset_index()
        df.columns = ["date", "price"]
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df["price"] = df["price"].round(2)
        df = df.dropna().sort_values("date").reset_index(drop=True)

        # Sanity check: reject obvious outliers
        if len(df) > 1:
            daily_change = df["price"].pct_change().abs()
            if (daily_change > 0.5).any():
                log.warning(
                    "Suspicious price spike detected (>50% in one day). Skipping update."
                )
                return None

        if (df["price"] <= 0).any():
            log.warning("Zero or negative BTC price detected. Skipping update.")
            return None

        log.info(
            f"Fetched {len(df)} rows. Latest: {df['date'].iloc[-1]} @ ${df['price'].iloc[-1]:,.2f}"
        )
        return df

    except Exception as e:
        log.error(f"Failed to fetch BTC data: {e}")
        return None


def save_btc(df: pd.DataFrame):
    DATA_DIR.mkdir(exist_ok=True)
    df.to_csv(BTC_FILE, index=False)
    log.info(f"Saved {len(df)} rows → {BTC_FILE}")


if __name__ == "__main__":
    df = fetch_btc()
    if df is not None:
        save_btc(df)
    else:
        log.warning("BTC data not updated — using existing file.")
