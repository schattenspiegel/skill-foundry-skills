# Evaluated solution recipes

## Recipe `pandas.validated-many-to-one`
**Use when:** join facts to unique dimensions without silent row multiplication.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd


def attach_customer(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    result = orders.merge(
        customers[["customer_id", "segment"]],
        on="customer_id",
        how="left",
        sort=False,
        validate="many_to_one",
        indicator=True,
    )
    if not result["_merge"].eq("both").all():
        raise ValueError("unmatched customer_id")
    return result[["order_id", "customer_id", "amount", "segment"]]
```
**Do not use when:** The requested abstraction or lifecycle differs from
`validated-customer-merge`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pandas.verify-join-cardinality`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd, pytest
from pandas.testing import assert_frame_equal
from solution import attach_customer


def test_cardinality_and_order() -> None:
    orders = pd.DataFrame({"order_id": [2, 1], "customer_id": [10, 20], "amount": [3, 4]})
    customers = pd.DataFrame({"customer_id": [20, 10], "segment": ["b", "a"]})
    actual = attach_customer(orders, customers)
    assert actual["order_id"].tolist() == [2, 1]
    assert actual["segment"].tolist() == ["a", "b"]
    with pytest.raises(pd.errors.MergeError):
        attach_customer(orders, pd.concat([customers, customers.iloc[[0]]]))
```
**Do not use when:** The requested abstraction or lifecycle differs from
`validated-customer-merge`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pandas.nullable-named-aggregation`
**Use when:** aggregate nullable values with an explicit missing-key policy.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd


def summarize_sales(frame: pd.DataFrame) -> pd.DataFrame:
    result = (
        frame.groupby("region", dropna=False, sort=True)
        .agg(
            order_count=("amount", "size"),
            known_amounts=("amount", "count"),
            total_amount=("amount", lambda values: values.sum(min_count=1)),
        )
        .reset_index()
    )
    return result.astype({"total_amount": "Float64"})
```
**Do not use when:** The requested abstraction or lifecycle differs from
`nullable-group-summary`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pandas.verify-missing-group-policy`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd
from solution import summarize_sales


def test_null_group_and_total() -> None:
    frame = pd.DataFrame(
        {"region": ["a", "a", None], "amount": pd.Series([1, None, None], dtype="Float64")}
    )
    result = summarize_sales(frame)
    assert len(result) == 2
    null_row = result[result["region"].isna()].iloc[0]
    assert null_row["order_count"] == 1 and null_row["known_amounts"] == 0
    assert pd.isna(null_row["total_amount"])
    assert str(result["total_amount"].dtype) == "Float64"
```
**Do not use when:** The requested abstraction or lifecycle differs from
`nullable-group-summary`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pandas.copy-on-write-update`
**Use when:** return an independent updated frame without chained assignment.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd


def mark_overdue(frame: pd.DataFrame, cutoff: pd.Timestamp) -> pd.DataFrame:
    if not frame.index.is_unique:
        raise ValueError("index must be unique")
    result = frame.copy()
    mask = result["due_at"].lt(cutoff) & result["paid_at"].isna()
    result.loc[:, "overdue"] = mask.astype("boolean")
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`copy-on-write-update`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `pandas.verify-input-independence`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pandas as pd, pytest
from solution import mark_overdue


def test_independent_update() -> None:
    frame = pd.DataFrame(
        {
            "due_at": pd.to_datetime(["2026-01-01", "2026-03-01"]),
            "paid_at": pd.to_datetime([None, None]),
        }
    )
    before = frame.copy(deep=True)
    result = mark_overdue(frame, pd.Timestamp("2026-02-01"))
    pd.testing.assert_frame_equal(frame, before)
    assert result["overdue"].tolist() == [True, False]
    assert str(result["overdue"].dtype) == "boolean"
    duplicate = frame.set_axis([0, 0])
    with pytest.raises(ValueError):
        mark_overdue(duplicate, pd.Timestamp("2026-02-01"))
```
**Do not use when:** The requested abstraction or lifecycle differs from
`copy-on-write-update`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
