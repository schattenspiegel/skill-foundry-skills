# Polars and PyArrow Boundaries object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `Polars DataFrame/Series`

Materialized columnar values with Polars dtypes. The critical boundary is: Conversion can rechunk, normalize, or reject Arrow representations.

## `Arrow Table/Array`

Immutable chunked columnar values plus Arrow schema. The critical boundary is: Chunking, offsets, dictionary encoding, and metadata are observable.

## `schema`

Field names, logical types, nullability, and metadata. The critical boundary is: Value equality alone cannot prove a boundary contract.

## `buffer ownership`

The lifetime and sharing of underlying memory. The critical boundary is: Zero-copy is conditional and must not be promised without buffer evidence.

## `storage boundary`

Parquet/IPC or consumer protocol after conversion. The critical boundary is: Test the final consumer semantics, not just an intermediate type.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
