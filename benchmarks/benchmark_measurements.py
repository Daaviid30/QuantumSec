"""Benchmark safe and fast projective sampling paths for one-qubit signals."""

import argparse
from collections.abc import Callable, Sequence
from functools import partial
from time import perf_counter

import numpy as np

from core.rng import SeededRNG
from qkd.primitives.measurements import MEASUREMENT_Z
from quantum import validation
from quantum.measures import sample_projective_outcome


def _elapsed(operation: Callable[[], object], calls: int, repeats: int) -> float:
    samples: list[float] = []
    for _ in range(repeats):
        start = perf_counter()
        for _ in range(calls):
            operation()
        samples.append(perf_counter() - start)
    return min(samples)


def run_benchmark(sizes: Sequence[int], repeats: int) -> None:
    """Print best-of-repeat wall times for the requested signal counts."""

    rho = np.identity(2, dtype=np.complex128) / 2.0
    print("signals,safe_s,fast_s,validation_s,eigvalsh_s,safe_over_fast")

    for size in sizes:
        safe_rng = SeededRNG(2026)
        fast_rng = SeededRNG(2026)
        safe_operation = partial(
            sample_projective_outcome,
            rho,
            MEASUREMENT_Z,
            safe_rng,
            validate_state=True,
        )
        safe_seconds = _elapsed(
            safe_operation,
            size,
            repeats,
        )
        fast_operation = partial(
            sample_projective_outcome,
            rho,
            MEASUREMENT_Z,
            fast_rng,
            validate_state=False,
        )
        fast_seconds = _elapsed(
            fast_operation,
            size,
            repeats,
        )
        validation_seconds = _elapsed(
            lambda: validation.validate_density_matrix(rho),
            size,
            repeats,
        )
        eigvalsh_seconds = _elapsed(lambda: np.linalg.eigvalsh(rho), size, repeats)
        ratio = safe_seconds / fast_seconds
        print(
            f"{size},{safe_seconds:.6f},{fast_seconds:.6f},"
            f"{validation_seconds:.6f},{eigvalsh_seconds:.6f},{ratio:.3f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=(1_000, 10_000, 100_000),
        help="Numbers of one-qubit signals to benchmark.",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=1,
        help="Repetitions per measurement; the best wall time is reported.",
    )
    args = parser.parse_args()

    if any(size <= 0 for size in args.sizes):
        parser.error("All sizes must be positive.")
    if args.repeats <= 0:
        parser.error("--repeats must be positive.")
    run_benchmark(args.sizes, args.repeats)


if __name__ == "__main__":
    main()
