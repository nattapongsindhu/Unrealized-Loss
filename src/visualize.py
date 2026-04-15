"""
visualize.py
Generate Three Asset Heartbreak Index chart.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from calculate_index import build_index

OUTPUT_DIR = Path(__file__).parent.parent / "output"

RELATIONSHIP_START = "2021-10-01"
RELATIONSHIP_END = "2024-08-23"


def plot(df: pd.DataFrame, save: bool = True):
    OUTPUT_DIR.mkdir(exist_ok=True)

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")

    # --- Lines ---
    ax.plot(
        df["date"],
        df["stamp_idx"],
        color="#4fc3f7",
        linewidth=2.2,
        label="Stamp (inflation proxy)",
        zorder=3,
    )
    ax.plot(
        df["date"],
        df["btc_idx"],
        color="#ffa726",
        linewidth=1.6,
        alpha=0.85,
        label="Bitcoin (USD)",
        zorder=2,
    )
    ax.plot(
        df["date"],
        df["heart_idx"],
        color="#ef5350",
        linewidth=2.4,
        label="Her Heart Value",
        zorder=4,
    )

    # --- Vertical markers ---
    ax.axvline(
        pd.Timestamp(RELATIONSHIP_START),
        color="#ffffff",
        linestyle="--",
        alpha=0.35,
        linewidth=1,
    )
    ax.axvline(
        pd.Timestamp(RELATIONSHIP_END),
        color="#ef5350",
        linestyle="--",
        alpha=0.6,
        linewidth=1.2,
    )

    ax.text(
        pd.Timestamp(RELATIONSHIP_END),
        ax.get_ylim()[1] * 0.97,
        " it ended here",
        color="#ef5350",
        fontsize=9,
        verticalalignment="top",
        alpha=0.85,
    )

    # --- Baseline ---
    ax.axhline(100, color="#ffffff", linestyle=":", alpha=0.15, linewidth=1)

    # --- Styling ---
    ax.set_title(
        "Three Things That Changed While You Were Together",
        color="#ffffff",
        fontsize=15,
        fontweight="bold",
        pad=18,
    )
    ax.set_xlabel("Date", color="#888888", fontsize=10)
    ax.set_ylabel("Indexed Value (100 = start)", color="#888888", fontsize=10)

    ax.tick_params(colors="#888888")
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    plt.xticks(rotation=30, ha="right")

    ax.legend(
        framealpha=0.15,
        labelcolor="white",
        facecolor="#1a1a2e",
        edgecolor="#333333",
        fontsize=10,
    )

    fig.text(
        0.5,
        0.01,
        "Only one of them was worth holding.",
        ha="center",
        color="#555555",
        fontsize=9,
        style="italic",
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])

    if save:
        out = OUTPUT_DIR / "chart.png"
        plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"Chart saved → {out}")
    else:
        plt.show()


if __name__ == "__main__":
    df = build_index()
    plot(df)
