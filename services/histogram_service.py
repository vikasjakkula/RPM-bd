"""
Generate a histogram image from user-provided numbers using matplotlib.
"""
import io
import logging
from typing import Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


def build_histogram(
    numbers: Sequence[float],
    title: str = "Distribution",
    xlabel: str = "Value",
    ylabel: str = "Frequency",
    bins: int | None = None,
    color: str = "#0f172a",
    edgecolor: str = "white",
) -> bytes:
    """
    Create a histogram from a list of numbers and return PNG bytes.
    """
    if not numbers:
        raise ValueError("At least one number is required")
    data = np.array(numbers, dtype=float)
    data = data[~np.isnan(data)]
    if len(data) == 0:
        raise ValueError("No valid numbers provided")
    if bins is None:
        bins = min(30, max(5, int(len(data) ** 0.5)))
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="#f8fafc")
    ax.set_facecolor("#f8fafc")
    ax.hist(data, bins=bins, color=color, edgecolor=edgecolor, linewidth=0.8)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()
