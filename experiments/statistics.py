"""Small statistical summaries required by the first experiment campaigns."""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import dataclass
from statistics import NormalDist

import numpy as np


@dataclass(frozen=True, slots=True)
class TimingSummary:
    n: int
    median: float
    q1: float
    q3: float
    iqr: float
    minimum: float
    maximum: float


@dataclass(frozen=True, slots=True)
class WilsonInterval:
    successes: int
    trials: int
    confidence: float
    estimate: float
    lower: float
    upper: float


def median_iqr(values: Iterable[float]) -> TimingSummary:
    """Summarize finite values with NumPy's linear percentile convention."""

    clean = tuple(values)
    if not clean:
        raise ValueError("values must contain at least one observation.")
    if any(isinstance(value, (bool, np.bool_)) for value in clean):
        raise ValueError("values must contain finite real numbers, not booleans.")
    try:
        array = np.asarray(clean, dtype=np.float64)
    except (TypeError, ValueError) as exc:
        raise ValueError("values must contain finite real numbers.") from exc
    if array.ndim != 1 or not np.all(np.isfinite(array)):
        raise ValueError("values must be a one-dimensional collection of finite numbers.")
    q1, median, q3 = np.percentile(array, (25.0, 50.0, 75.0), method="linear")
    return TimingSummary(
        n=int(array.size),
        median=float(median),
        q1=float(q1),
        q3=float(q3),
        iqr=float(q3 - q1),
        minimum=float(np.min(array)),
        maximum=float(np.max(array)),
    )


def wilson_interval(
    successes: int,
    trials: int,
    confidence: float = 0.95,
) -> WilsonInterval:
    """Return the two-sided Wilson score interval (not Clopper-Pearson exact)."""

    if isinstance(successes, bool) or not isinstance(successes, int):
        raise ValueError("successes must be an integer.")
    if isinstance(trials, bool) or not isinstance(trials, int) or trials <= 0:
        raise ValueError("trials must be a positive integer.")
    if not 0 <= successes <= trials:
        raise ValueError("successes must lie between zero and trials.")
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
        raise ValueError("confidence must be a finite probability.")
    clean_confidence = float(confidence)
    if not math.isfinite(clean_confidence) or not 0.0 < clean_confidence < 1.0:
        raise ValueError("confidence must lie strictly between zero and one.")

    estimate = successes / trials
    z = NormalDist().inv_cdf(0.5 + clean_confidence / 2.0)
    z_squared = z * z
    denominator = 1.0 + z_squared / trials
    center = (estimate + z_squared / (2.0 * trials)) / denominator
    radius = z * math.sqrt(estimate * (1.0 - estimate) / trials + z_squared / (4.0 * trials**2)) / denominator
    return WilsonInterval(
        successes=successes,
        trials=trials,
        confidence=clean_confidence,
        estimate=estimate,
        # Cancellation at the boundaries must not put an endpoint on the
        # wrong side of its own point estimate.
        lower=max(0.0, min(estimate, center - radius)),
        upper=min(1.0, max(estimate, center + radius)),
    )
