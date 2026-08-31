"""Stateless security-length metrics for the current asymptotic BB84 model."""

from math import floor, log2

import numpy as np


def _probability(value: float, *, name: str) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (float, int, np.floating, np.integer)):
        raise ValueError(f"{name} must be a finite probability. Got {value!r}.")
    result = float(value)
    if not np.isfinite(result) or not 0.0 <= result <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1]. Got {result}.")
    return result


def _non_negative_int(value: object, *, name: str) -> int:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, np.integer)):
        raise ValueError(f"{name} must be a non-negative integer. Got {value!r}.")
    result = int(value)
    if result < 0:
        raise ValueError(f"{name} must be non-negative. Got {result}.")
    return result


def binary_entropy(p: float) -> float:
    """Return binary Shannon entropy ``h2(p)`` with exact endpoint handling."""

    probability = _probability(p, name="p")
    if probability in (0.0, 1.0):
        return 0.0
    return -probability * log2(probability) - (1.0 - probability) * log2(1.0 - probability)


def asymptotic_bb84_secret_length(
    n_candidate: int,
    estimated_qber: float,
    leak_ec: int,
    leak_verification: int,
    *,
    security_margin_bits: int = 0,
) -> int:
    """Estimate extractable bits under the simulator's asymptotic BB84 model.

    The symmetric-channel phase-error estimate is the sampled QBER. Actual
    simulated reconciliation leakage replaces an ideal ``n*h2(Q)`` term and is
    therefore subtracted exactly once. This is not a composable finite-key proof.
    """

    n = _non_negative_int(n_candidate, name="n_candidate")
    qber = _probability(estimated_qber, name="estimated_qber")
    reconciliation_leakage = _non_negative_int(leak_ec, name="leak_ec")
    verification_leakage = _non_negative_int(leak_verification, name="leak_verification")
    margin = _non_negative_int(security_margin_bits, name="security_margin_bits")
    length = floor(n * (1.0 - binary_entropy(qber)) - reconciliation_leakage - verification_leakage - margin)
    return max(0, min(n, length))
