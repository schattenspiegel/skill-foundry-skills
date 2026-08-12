# Evaluated solution recipes

## Recipe `boundary.timestamp-schema-roundtrip`
**Use when:** preserve timestamp units, timezone, nulls, and nanoseconds.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import polars as pl
import pyarrow as pa


def roundtrip_timestamp(table: pa.Table) -> pa.Table:
    field = table.schema.field("event_time")
    expected = pa.timestamp("ns", tz="UTC")
    if field.type != expected or table.column("event_time").null_count == table.num_rows:
        raise ValueError("event_time must be timestamp[ns, UTC] with a value")
    result = pl.from_arrow(table).to_arrow()
    if result.schema.field("event_time").type != expected:
        raise RuntimeError("timestamp dtype changed")
    if (
        not result.column("event_time")
        .combine_chunks()
        .equals(table.column("event_time").combine_chunks())
    ):
        raise RuntimeError("timestamp values changed")
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`timestamp-ns-timezone-roundtrip`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `boundary.verify-nanosecond-timezone-values`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import polars as pl
import pyarrow as pa
from solution import roundtrip_timestamp


def test_ns_timezone_and_null() -> None:
    array = pa.array([1_700_000_000_000_000_123, None], type=pa.timestamp("ns", tz="UTC"))
    table = pa.table({"event_time": array})
    result = roundtrip_timestamp(table)
    assert result.schema.field("event_time").type == pa.timestamp("ns", tz="UTC")
    assert result.column("event_time").combine_chunks().equals(array)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`timestamp-ns-timezone-roundtrip`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `boundary.chunk-normalization`
**Use when:** normalize chunks while preserving typed nullable values.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import polars as pl
import pyarrow as pa


def normalize_table(table: pa.Table) -> pa.Table:
    if (
        table.schema.names != ["id", "score"]
        or table.schema.field("id").type != pa.int64()
        or table.schema.field("score").type != pa.float64()
    ):
        raise ValueError("unexpected schema")
    if table.column("id").null_count:
        raise ValueError("id contains null")
    result = pl.from_arrow(table).rechunk().to_arrow()
    if any(column.num_chunks != 1 for column in result.columns):
        raise RuntimeError("columns were not rechunked")
    if not result.equals(table.combine_chunks(), check_metadata=False):
        raise RuntimeError("values changed")
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`chunked-nullable-table`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `boundary.verify-nullability-and-values`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pyarrow as pa
import pytest
from solution import normalize_table


def test_chunks_and_null_policy() -> None:
    table = pa.Table.from_arrays(
        [
            pa.chunked_array([[1, 2], [3]], type=pa.int64()),
            pa.chunked_array([[1.5], [None, 3.5]], type=pa.float64()),
        ],
        names=["id", "score"],
    )
    result = normalize_table(table)
    assert all(column.num_chunks == 1 for column in result.columns)
    with pytest.raises(ValueError):
        normalize_table(
            pa.table({"id": pa.array([1, None], type=pa.int64()), "score": pa.array([1.0, 2.0])})
        )
```
**Do not use when:** The requested abstraction or lifecycle differs from
`chunked-nullable-table`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `boundary.dictionary-nested-policy`
**Use when:** cross categorical and nested columns without silent semantic loss.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import polars as pl
import pyarrow as pa


def cross_nested(table: pa.Table) -> pa.Table:
    category = table.schema.field("category").type
    tags = table.schema.field("tags").type
    if (
        not pa.types.is_dictionary(category)
        or category.index_type != pa.int32()
        or category.value_type != pa.string()
    ):
        raise ValueError("category must be dictionary<int32, string>")
    if not (pa.types.is_list(tags) and tags.value_type == pa.string()):
        raise ValueError("tags must be list<string>")
    result = pl.from_arrow(table).to_arrow()
    source_category = table.column("category").combine_chunks().dictionary_decode()
    output_category = result.column("category").combine_chunks()
    if pa.types.is_dictionary(output_category.type):
        output_category = output_category.dictionary_decode()
    if not output_category.cast(source_category.type).equals(source_category):
        raise RuntimeError("decoded category values changed")
    source_tags = table.column("tags").combine_chunks()
    output_tags = result.column("tags").combine_chunks()
    output_value_type = output_tags.type.value_type
    if not (
        (pa.types.is_list(output_tags.type) or pa.types.is_large_list(output_tags.type))
        and (pa.types.is_string(output_value_type) or pa.types.is_large_string(output_value_type))
    ):
        raise RuntimeError("nested tags type changed incompatibly")
    if not output_tags.cast(source_tags.type).equals(source_tags):
        raise RuntimeError("nested tags changed")
    return result
```
**Do not use when:** The requested abstraction or lifecycle differs from
`dictionary-and-list-contract`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `boundary.verify-decoded-and-nested-values`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import pyarrow as pa
from solution import cross_nested


def test_dictionary_and_nested_values() -> None:
    category = pa.DictionaryArray.from_arrays(
        pa.array([0, 1, None], type=pa.int32()), pa.array(["a", "b"])
    )
    tags = pa.array([["x", "y"], None, []], type=pa.list_(pa.string()))
    table = pa.table({"category": category, "tags": tags})
    result = cross_nested(table)
    assert result.column("tags").combine_chunks().cast(tags.type).equals(tags)
    assert result.column("category").to_pylist() == ["a", "b", None]
```
**Do not use when:** The requested abstraction or lifecycle differs from
`dictionary-and-list-contract`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
