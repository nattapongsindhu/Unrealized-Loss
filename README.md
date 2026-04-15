# Three Asset Heartbreak Index

**Stamp. Bitcoin. Her Heart.**

!\[Last Updated](https://img.shields.io/github/last-commit/nattapongsindhu/three-asset-heartbreak-index?label=last%20updated\&color=green)
!\[Python](https://img.shields.io/badge/python-3.11-blue)
!\[Data](https://img.shields.io/badge/BTC-CoinGecko-orange)
!\[Stamp](https://img.shields.io/badge/stamp-USPS-blue)

> A data project comparing three assets over the same time period.  
> One is guaranteed by the US government.  
> One is guaranteed by no one.  
> One was guaranteed by her.

\---

## Sample Output

!\[chart](output/chart.png)

\---

## How It Works

Three assets are indexed to **100** at the relationship start date (`2021-10-01`) and tracked through to today:

|Asset|Source|Behavior|
|-|-|-|
|🟦 Stamp|USPS historical rate table|Step-function increases|
|🟠 Bitcoin|CoinGecko API (free)|Volatile daily close price|
|🔴 Her Heart|Mathematical formula|Exponential decay after end date|

**Heart Index formula:**

```
heart(t) = 100 × e^(−0.003 × days\_since\_end)
Half-life: \~231 days. Floor: 0. No recovery.
```

\---

## How to Run Locally

```bash
# Clone
git clone https://github.com/nattapongsindhu/Unrealized-Loss
cd three-asset-heartbreak-index

# Install
pip install -r requirements.txt

# Fetch BTC data
python src/fetch\_btc.py

# Generate Heart Index
python src/generate\_heart.py

# Print metrics
python src/calculate\_index.py

# Generate chart → output/chart.png
python src/visualize.py
```

\---

## Methodology

* All series normalized to **100** at `2021-10-01`
* BTC: actual daily closing price from CoinGecko
* Stamp: forward-filled from USPS historical rate changes
* Heart: `100 \* e^(-0.003 \* t)` where `t = days since 2024-08-23`

**Metrics calculated per asset:**

* Total return %
* Max drawdown %
* Volatility (std dev of daily % change)
* Final value

\---

## Automation

GitHub Actions runs every day at **09:00 UTC**:

1. Fetches latest BTC price
2. Extends Heart Index by one day
3. Regenerates `output/chart.png`
4. Auto-commits → keeps contribution graph green 🟩

\---

## Data Sources

* **Stamp prices:** USPS historical rate table (static CSV, manually maintained)
* **Bitcoin:** [CoinGecko public API](https://www.coingecko.com/en/api) — no API key required
* **Heart Index:** mathematically generated

\---

*"Only one of them was worth holding."*

