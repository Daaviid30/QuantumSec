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


def test_wilson_interval_contains_observed_estimate() -> None:
    interval = wilson_interval(25, 100)
    assert interval.estimate == 0.25
    assert interval.lower < interval.estimate < interval.upper
    assert interval.confidence == 0.95


@pytest.mark.parametrize("arguments", [(-1, 10), (11, 10), (0, 0)])
def test_wilson_interval_rejects_invalid_counts(arguments) -> None:
    with pytest.raises(ValueError):
        wilson_interval(*arguments)
