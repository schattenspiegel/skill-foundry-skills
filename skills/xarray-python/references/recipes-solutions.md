# Evaluated solution recipes

## Recipe `xarray.exact-aligned-arithmetic`
**Use when:** prevent silent coordinate union during arithmetic.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import xarray as xr


def exact_ratio(numerator: xr.DataArray, denominator: xr.DataArray) -> xr.DataArray:
    left, right = xr.align(numerator, denominator, join="exact", copy=False)
    if bool((right <= 0).any()):
        bad = right.where(right <= 0, drop=True)
        raise ValueError(f"nonpositive denominator at {bad.coords}")
    result = left / right
    result.name = f"{numerator.name or 'value'}_ratio"
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`exact-coordinate-alignment`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `xarray.verify-coordinate-contract`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pytest
import xarray as xr
from solution import exact_ratio


def test_exact_labels() -> None:
    left = xr.DataArray([2.0, 6.0], dims="city", coords={"city": ["a", "b"]}, name="sales")
    right = xr.DataArray([1.0, 3.0], dims="city", coords={"city": ["a", "b"]})
    result = exact_ratio(left, right)
    assert result.values.tolist() == [2.0, 2.0]
    assert result.name == "sales_ratio"
    with pytest.raises(ValueError):
        exact_ratio(left, right.assign_coords(city=["b", "a"]))
```
**Do not use when:** The requested abstraction or lifecycle differs from
`exact-coordinate-alignment`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `xarray.mask-aware-weighted-reduction`
**Use when:** compute weighted means with explicit missing-data support.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
import xarray as xr


def weighted_time_mean(values: xr.DataArray, weights: xr.DataArray) -> xr.DataArray:
    values, weights = xr.align(values, weights, join="exact", copy=False)
    if weights.dims != ("time",) or bool((weights < 0).any()) or not np.isfinite(weights).all():
        raise ValueError("weights must be finite, nonnegative, and one-dimensional over time")
    effective = weights.where(values.notnull())
    denominator = effective.sum("time")
    if bool((denominator <= 0).any()):
        raise ValueError("zero effective weight")
    return (values * effective).sum("time", skipna=True) / denominator
```
**Do not use when:** The requested abstraction or lifecycle differs from
`masked-weighted-mean`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `xarray.verify-weight-normalization`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import numpy as np
import pytest
import xarray as xr
from solution import weighted_time_mean


def test_masked_normalization() -> None:
    values = xr.DataArray(
        [[1.0, np.nan], [3.0, 10.0]], dims=("time", "site"), coords={"time": [0, 1]}
    )
    weights = xr.DataArray([1.0, 3.0], dims="time", coords={"time": [0, 1]})
    result = weighted_time_mean(values, weights)
    assert result.values.tolist() == [2.5, 10.0]
    with pytest.raises(ValueError):
        weighted_time_mean(values, weights * 0)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`masked-weighted-mean`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `xarray.time-resample-contract`
**Use when:** aggregate irregular observations into explicit daily bins.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd
import xarray as xr


def daily_total(values: xr.DataArray) -> xr.DataArray:
    index = values.get_index("time")
    if (
        not isinstance(index, pd.DatetimeIndex)
        or not index.is_unique
        or not index.is_monotonic_increasing
    ):
        raise ValueError("time must be a unique sorted DatetimeIndex")
    result = values.resample(time="1D").sum(skipna=True, min_count=1, keep_attrs=True)
    result.name = "daily_total"
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`sorted-daily-resample`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `xarray.verify-bin-and-order-semantics`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd
import pytest
import xarray as xr
from solution import daily_total


def test_bins_and_order_guard() -> None:
    values = xr.DataArray(
        [1.0, 2.0, 4.0],
        dims="time",
        coords={
            "time": pd.to_datetime(["2026-01-01T01:00", "2026-01-01T03:00", "2026-01-03T00:00"])
        },
        attrs={"unit": "kg"},
    )
    result = daily_total(values)
    assert result.values[[0, 2]].tolist() == [3.0, 4.0]
    assert result.attrs["unit"] == "kg"
    with pytest.raises(ValueError):
        daily_total(values.isel(time=[1, 0, 2]))
```
**Do not use when:** The requested abstraction or lifecycle differs from
`sorted-daily-resample`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
