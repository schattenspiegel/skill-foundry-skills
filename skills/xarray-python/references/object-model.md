# Xarray Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `DataArray`

N-dimensional values plus named dimensions and coordinates. The critical boundary is: Operations align by coordinate labels, not raw axis position.

## `Dataset`

A mapping of aligned named variables with shared coordinates. The critical boundary is: Variables may have different dimension subsets and dtypes.

## `coordinate/index`

Labels that define selection and alignment semantics. The critical boundary is: Duplicates, order, calendars, and join policy affect correctness.

## `lazy chunked array`

A deferred Dask-backed computation graph. The critical boundary is: Chunking and `.compute()` boundaries control execution and memory.

## `encoding`

Storage metadata separate from in-memory attrs and dtype. The critical boundary is: Round-trip requirements must be stated at I/O boundaries.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
