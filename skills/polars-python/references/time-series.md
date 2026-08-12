# Time-series rules

Load this reference for dynamic buckets, trailing temporal windows, rolling
expressions, time zones, or daylight-saving behavior.

## Choose the temporal shape

| Contract | Operation |
|---|---|
| One row per fixed time bucket | `group_by_dynamic`. |
| One trailing window for every observation | `rolling` or an installed `rolling_*_by` expression. |
| One fixed number of neighboring rows | Row-count rolling expression after deterministic ordering. |
| Cumulative, lag, or diff within entities | `.over(entity, order_by=time_and_tie_breaker)`. |

For dynamic and trailing time windows, establish the time column's dtype,
sortedness within grouping keys, bucket/window duration, offset, closed sides,
labels, and expected empty buckets. Calendar durations such as a day or month
can differ from fixed elapsed durations across daylight-saving transitions.
Test the boundary instant on each side, not only a value in the middle.

## Time-zone decision

| Input meaning | Action |
|---|---|
| Naive values already represent wall time in a named zone | Attach or replace the time zone, with an explicit ambiguous/nonexistent-time policy. |
| Aware instants must be displayed or grouped in another zone | Convert the time zone; do not replace it. |
| Sources mix zones or naive meanings are unknown | Normalize at the input boundary or stop for a domain decision. |

Changing a zone label and converting an instant are different operations.
Include a daylight-saving transition when local calendar boundaries affect the
result.

```python
daily = (
    events.with_columns(local_time=pl.col("event_time").dt.convert_time_zone("Europe/Berlin"))
    .sort("local_time")
    .group_by_dynamic(
        "local_time",
        every="1d",
        period="1d",
        closed="left",
        label="left",
    )
    .agg(pl.col("revenue").sum())
)
```

This is a local-calendar bucket, not a fixed 24-hour UTC bin. Keep the zone on
the bucket label or convert it to the caller's required output explicitly.

## Verification

Test unsorted input, equal timestamps with a tie-breaker, exact boundaries,
empty periods when relevant, null timestamps, multiple groups, and a
daylight-saving transition for local calendar semantics. Inspect the installed
API before fixing `closed`, `label`, offset, or rolling keyword names in durable
code.
