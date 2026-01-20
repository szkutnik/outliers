"""Outlier detection helpers using a robust modified z-score."""

from __future__ import annotations

from statistics import median
from typing import Iterable, List


MAD_SCALE = 0.6745


def modified_z_scores(values: Iterable[float]) -> List[float]:
    """Return modified z-scores for each value using the median absolute deviation.

    Args:
        values: Iterable of numeric values.

    Returns:
        List of modified z-scores in the same order as the input.
    """

    data = list(values)
    if not data:
        return []

    med = median(data)
    deviations = [abs(value - med) for value in data]
    mad = median(deviations)

    if mad == 0:
        mean_deviation = sum(deviations) / len(deviations)
        if mean_deviation == 0:
            return [0.0 for _ in data]
        return [MAD_SCALE * (value - med) / mean_deviation for value in data]

    return [MAD_SCALE * (value - med) / mad for value in data]


def detect_outliers(values: Iterable[float], threshold: float = 3.5) -> List[bool]:
    """Detect outliers using modified z-scores.

    Args:
        values: Iterable of numeric values.
        threshold: Absolute z-score threshold to flag an outlier.

    Returns:
        List of booleans indicating which entries are outliers.
    """

    scores = modified_z_scores(values)
    return [abs(score) > threshold for score in scores]
