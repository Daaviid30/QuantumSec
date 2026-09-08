import pytest

from experiments import median_iqr, wilson_interval


def test_median_iqr_reports_requested_summary() -> None:
    summary = median_iqr((1.0, 2.0, 3.0, 4.0, 5.0))
    assert summary.n == 5
    assert summary.median == 3.0
    assert summary.q1 == 2.0
    assert summary.q3 == 4.0
    assert summary.iqr == 2.0
    assert summary.minimum == 1.0
    assert summary.maximum == 5.0


def test_median_iqr_uses_linear_interpolation_for_even_sample() -> None:
    summary = median_iqr((1.0, 2.0, 3.0, 4.0))
    assert summary.median == 2.5
    assert summary.q1 == 1.75
    assert summary.q3 == 3.25


@pytest.mark.parametrize("values", [(float("nan"),), (float("inf"),), (True,)])
def test_median_iqr_rejects_non_finite_values_and_booleans(values) -> None:
    with pytest.raises(ValueError):
        median_iqr(values)


def test_wilson_interval_contains_observed_estimate() -> None:
    interval = wilson_interval(25, 100)
    assert interval.estimate == 0.25
    assert interval.lower < interval.estimate < interval.upper
    assert interval.confidence == 0.95


@pytest.mark.parametrize(("successes", "expected_edge"), [(0, "lower"), (100, "upper")])
def test_wilson_interval_handles_extreme_observations(successes, expected_edge) -> None:
    interval = wilson_interval(successes, 100)
    assert getattr(interval, expected_edge) == successes / 100
    assert 0.0 <= interval.lower <= interval.upper <= 1.0


def test_wilson_interval_accepts_one_trial() -> None:
    interval = wilson_interval(1, 1)
    assert interval.estimate == 1.0
    assert interval.upper == 1.0


@pytest.mark.parametrize("arguments", [(-1, 10), (11, 10), (0, 0)])
def test_wilson_interval_rejects_invalid_counts(arguments) -> None:
    with pytest.raises(ValueError):
        wilson_interval(*arguments)
