# Evaluated solution recipes

## Recipe `statsmodels.formula-ols-robust`
**Use when:** fit a categorical regression with robust covariance.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
import statsmodels.formula.api as smf


def fit_outcome(frame):
    if (
        frame["group"].nunique(dropna=False) < 2
        or not np.isfinite(frame[["outcome", "exposure"]]).all().all()
    ):
        raise ValueError("invalid design data")
    result = smf.ols("outcome ~ exposure + C(group)", data=frame, missing="raise").fit(
        cov_type="HC3"
    )
    if result.nobs != len(frame) or not np.isfinite(result.params).all():
        raise RuntimeError("fit contract failed")
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`formula-ols-hc3`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `statsmodels.verify-design-and-covariance`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd
import pytest
from solution import fit_outcome


def test_formula_and_covariance() -> None:
    frame = pd.DataFrame(
        {
            "outcome": [1, 2, 2, 4, 5, 6],
            "exposure": [0, 1, 0, 1, 2, 3],
            "group": ["a", "a", "b", "b", "a", "b"],
        }
    )
    result = fit_outcome(frame)
    assert result.cov_type == "HC3"
    assert "C(group)[T.b]" in result.params
    with pytest.raises(ValueError):
        fit_outcome(frame.assign(group="a"))
```
**Do not use when:** The requested abstraction or lifecycle differs from
`formula-ols-hc3`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `statsmodels.prediction-summary-frame`
**Use when:** return distinct prediction uncertainty targets.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np

COLUMNS = ["mean", "mean_ci_lower", "mean_ci_upper", "obs_ci_lower", "obs_ci_upper"]


def prediction_intervals(result, new_data, alpha: float = 0.05):
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between zero and one")
    frame = result.get_prediction(new_data).summary_frame(alpha=alpha)
    output = frame[COLUMNS]
    if not np.isfinite(output.to_numpy()).all():
        raise RuntimeError("nonfinite prediction interval")
    if not (
        (output.mean_ci_lower <= output["mean"]) & (output["mean"] <= output.mean_ci_upper)
    ).all():
        raise RuntimeError("invalid mean interval")
    return output
```
**Do not use when:** The requested abstraction or lifecycle differs from
`mean-and-observation-intervals`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `statsmodels.verify-interval-semantics`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd
import statsmodels.formula.api as smf
from solution import prediction_intervals


def test_both_interval_types() -> None:
    frame = pd.DataFrame({"x": [0, 1, 2, 3, 4], "y": [0.1, 1.2, 1.9, 3.2, 3.8]})
    result = smf.ols("y ~ x", frame).fit()
    intervals = prediction_intervals(result, pd.DataFrame({"x": [1.5]}))
    assert list(intervals) == [
        "mean",
        "mean_ci_lower",
        "mean_ci_upper",
        "obs_ci_lower",
        "obs_ci_upper",
    ]
    assert (
        intervals.loc[0, "obs_ci_upper"] - intervals.loc[0, "obs_ci_lower"]
        >= intervals.loc[0, "mean_ci_upper"] - intervals.loc[0, "mean_ci_lower"]
    )
```
**Do not use when:** The requested abstraction or lifecycle differs from
`mean-and-observation-intervals`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `statsmodels.hac-ordered-fit`
**Use when:** use HAC covariance only on verified time ordering.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
import statsmodels.formula.api as smf


def fit_hac(frame, maxlags: int):
    if not frame["time"].is_unique or not frame["time"].is_monotonic_increasing:
        raise ValueError("time must be unique and sorted")
    if type(maxlags) is not int or not 1 <= maxlags < len(frame):
        raise ValueError("invalid maxlags")
    result = smf.ols("y ~ x", data=frame, missing="raise").fit(
        cov_type="HAC", cov_kwds={"maxlags": maxlags}
    )
    if result.nobs != len(frame) or not np.isfinite(result.params).all():
        raise RuntimeError("fit contract failed")
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`ordered-hac-regression`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `statsmodels.verify-time-and-lag-contract`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd
import pytest
from solution import fit_hac


def test_order_and_lag() -> None:
    frame = pd.DataFrame(
        {
            "time": pd.date_range("2026-01-01", periods=8),
            "x": range(8),
            "y": [0, 1, 1, 3, 4, 4, 6, 7],
        }
    )
    assert fit_hac(frame, 2).cov_type == "HAC"
    with pytest.raises(ValueError):
        fit_hac(frame.iloc[::-1], 2)
    with pytest.raises(ValueError):
        fit_hac(frame, 8)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`ordered-hac-regression`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
