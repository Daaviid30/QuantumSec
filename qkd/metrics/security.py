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
    candidate_length: int,
    *,
    phase_error_bound: float,
    reconciliation_leakage: int,
    verification_leakage: int,
    security_margin_bits: int = 0,
) -> int:
    """Estimate extractable bits from an explicit asymptotic phase-error bound.

    The modeled length is ``floor(n * (1 - h2(e_phase)) - leak_ec -
    leak_verification - margin)``. Actual simulated reconciliation leakage
    replaces an ideal bit-error entropy term and is subtracted exactly once.
    ``phase_error_bound`` must be justified by the calling protocol; aggregate
    QBER is not automatically such a bound. This is not a composable finite-key
    proof.
    """

    n = _non_negative_int(candidate_length, name="candidate_length")
    phase_error = _probability(phase_error_bound, name="phase_error_bound")
    if phase_error > 0.5:
        raise ValueError(
            f"phase_error_bound must lie in [0, 0.5] for the asymptotic entropy model. Got {phase_error}."
        )
    reconciliation = _non_negative_int(reconciliation_leakage, name="reconciliation_leakage")
    verification = _non_negative_int(verification_leakage, name="verification_leakage")
    margin = _non_negative_int(security_margin_bits, name="security_margin_bits")
    length = floor(n * (1.0 - binary_entropy(phase_error)) - reconciliation - verification - margin)
    if length <= 0:
        return 0
    return length
