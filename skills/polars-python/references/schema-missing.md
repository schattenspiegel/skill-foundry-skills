# Schema and missing-data rules

Load this reference when inference, casting, empty input, nested fields, identifiers, temporal values, nulls, or `NaN` can change the result.

## Establish schema cheaply

For a lazy plan, call `collect_schema()` rather than materializing rows. Pin scan-time schema or overrides when:

- identifiers have leading zeros or fixed width;
- early rows are not representative;
- files can be header-only or empty;
- temporal parsing or time zones are contractual;
- dirty sentinels must become null;
- nested fields must retain exact inner types.

Do not set `ignore_errors` merely to make ingestion finish. Decide whether bad input must raise, become null, or be quarantined, then test that policy.

For a stable CSV contract, pin the schema at the scan boundary rather than
collecting a sample and re-lazifying it:

```python
def scan_orders(path: str) -> pl.LazyFrame:
    return pl.scan_csv(
        path,
        schema_overrides={
            "order_id": pl.UInt32,
            "customer_id": pl.UInt32,
            "amount": pl.Float64,
            "is_refund": pl.Boolean,
        },
    )
```

Test a header-only file and a bad value appearing after representative rows.
Construction must remain lazy; the bad value should fail at collection when
strict ingestion is the contract.

## Cast decision

| Condition | Action |
|---|---|
| Every value must be valid | Use strict casting and allow invalid input to fail. |
| Invalid values are defined to become null | Use non-strict casting and assert/count introduced nulls. |
| Conversion changes domain or may lose information | Reject it or require an explicit upstream policy. |
| Empty construction cannot infer a stable type | Supply an explicit schema. |

Never cast identifiers through floating point. Do not cast join keys to strings merely to silence a mismatch; leading zeros, normalization, and domain identity are semantic decisions.

## Null is not NaN

`null` represents missing data for any dtype. `NaN` is a floating-point value. They use separate predicates and fill operations:

```python
clean = frame.with_columns(
    pl.col("reading").is_nan().fill_null(False).alias("invalid_reading"),
    pl.col("reading").fill_nan(0.0).alias("reading"),
)
```

The example converts `NaN` while leaving null untouched. Do not use it unless that matches the business rule. Test normal values, null, `NaN`, infinities when allowed, and aggregation behavior.

Filtering on a comparison drops null rows because a null predicate is not true. If null rows must survive, encode that branch explicitly. Check null-key join behavior separately; null equality is disabled by default in current releases.
