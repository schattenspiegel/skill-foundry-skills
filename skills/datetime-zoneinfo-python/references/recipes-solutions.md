# Evaluated solution recipes

## Recipe `datetime.resolve-local`
**Use when:** reject nonexistent local times and require an ambiguity choice.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from datetime import UTC, datetime
from zoneinfo import ZoneInfo


def resolve_local(naive: datetime, zone_name: str, fold: int | None = None) -> datetime:
    if naive.tzinfo is not None:
        raise ValueError("expected a naive wall time")
    if fold not in (None, 0, 1):
        raise ValueError("fold must be 0 or 1")
    zone = ZoneInfo(zone_name)
    valid: dict[int, datetime] = {}
    for candidate_fold in (0, 1):
        candidate = naive.replace(tzinfo=zone, fold=candidate_fold)
        back = candidate.astimezone(UTC).astimezone(zone)
        if back.replace(tzinfo=None) == naive and back.fold == candidate_fold:
            valid[candidate_fold] = candidate
    if not valid:
        raise ValueError("nonexistent local time")
    if len(valid) == 2 and valid[0].utcoffset() != valid[1].utcoffset():
        if fold is None:
            raise ValueError("ambiguous local time requires fold")
        return valid[fold]
    return next(iter(valid.values()))
```
**Do not use when:** The requested abstraction or lifecycle differs from
`resolve-local-wall-time`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `datetime.verify-gap-fold`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from datetime import datetime
import pytest
from solution import resolve_local


def test_gap_and_fold() -> None:
    with pytest.raises(ValueError, match="nonexistent"):
        resolve_local(datetime(2026, 3, 29, 2, 30), "Europe/Berlin")
    ambiguous = datetime(2026, 10, 25, 2, 30)
    with pytest.raises(ValueError, match="ambiguous"):
        resolve_local(ambiguous, "Europe/Berlin")
    first = resolve_local(ambiguous, "Europe/Berlin", 0)
    second = resolve_local(ambiguous, "Europe/Berlin", 1)
    assert first.utcoffset() != second.utcoffset()
```
**Do not use when:** The requested abstraction or lifecycle differs from
`resolve-local-wall-time`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `datetime.weekly-civil-recurrence`
**Use when:** preserve a recurring local appointment across DST.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo


def resolve_local(naive: datetime, zone_name: str) -> datetime:
    zone = ZoneInfo(zone_name)
    valid = []
    for fold in (0, 1):
        candidate = naive.replace(tzinfo=zone, fold=fold)
        back = candidate.astimezone(UTC).astimezone(zone)
        if back.replace(tzinfo=None) == naive:
            valid.append(candidate)
    if not valid:
        raise ValueError("nonexistent local time")
    if len(valid) == 2 and valid[0].utcoffset() != valid[1].utcoffset():
        raise ValueError("ambiguous local time requires an explicit policy")
    return valid[0]


def weekly_instants(
    start_date: date, local_time: time, zone_name: str, count: int
) -> list[datetime]:
    if count < 0:
        raise ValueError("count must be nonnegative")
    if local_time.tzinfo is not None:
        raise ValueError("local_time must be naive")
    return [
        resolve_local(
            datetime.combine(start_date + timedelta(days=7 * index), local_time), zone_name
        ).astimezone(UTC)
        for index in range(count)
    ]
```
**Do not use when:** The requested abstraction or lifecycle differs from
`weekly-local-recurrence`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `datetime.verify-dst-recurrence`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from datetime import date, time
from zoneinfo import ZoneInfo
from solution import weekly_instants


def test_wall_clock_survives_dst() -> None:
    values = weekly_instants(date(2026, 3, 22), time(9, 0), "Europe/Berlin", 3)
    local = [value.astimezone(ZoneInfo("Europe/Berlin")) for value in values]
    assert [(value.hour, value.minute) for value in local] == [(9, 0)] * 3
    assert (values[1] - values[0]).total_seconds() == 7 * 86400 - 3600
```
**Do not use when:** The requested abstraction or lifecycle differs from
`weekly-local-recurrence`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `datetime.half-open-window`
**Use when:** apply an explicit half-open UTC interval contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from datetime import UTC, datetime


def contains_instant(start: datetime, end: datetime, value: datetime) -> bool:
    if any(item.tzinfo is None or item.utcoffset() is None for item in (start, end, value)):
        raise ValueError("all values must be aware")
    start_utc, end_utc, value_utc = (item.astimezone(UTC) for item in (start, end, value))
    if end_utc < start_utc:
        raise ValueError("end precedes start")
    return start_utc <= value_utc < end_utc
```
**Do not use when:** The requested abstraction or lifecycle differs from
`half-open-instant-window`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `datetime.verify-window-boundaries`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
from datetime import UTC, datetime, timedelta, timezone
import pytest
from solution import contains_instant


def test_boundaries_and_offsets() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    end = start + timedelta(hours=1)
    assert contains_instant(start, end, start)
    assert not contains_instant(start, end, end)
    assert contains_instant(
        start, end, datetime(2026, 1, 1, 1, 30, tzinfo=timezone(timedelta(hours=1)))
    )
    with pytest.raises(ValueError):
        contains_instant(start.replace(tzinfo=None), end, start)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`half-open-instant-window`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
