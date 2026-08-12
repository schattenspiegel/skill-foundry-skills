# pandas Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `Series`

A one-dimensional labeled array with one dtype. The critical boundary is: Operations align by index labels unless explicitly converted to positions.

## `DataFrame`

A two-dimensional labeled collection of Series. The critical boundary is: Column dtypes and index semantics remain independent.

## `Index`

The label and alignment key for an axis. The critical boundary is: Duplicate labels can make selection and joins non-scalar.

## `GroupBy`

A deferred split/combine object. The critical boundary is: Complete it with an explicit aggregation, transform, filter, or apply contract.

## `Extension dtype`

Nullable or semantic dtype beyond NumPy primitives. The critical boundary is: Preserve it explicitly across missing values and interchange.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
