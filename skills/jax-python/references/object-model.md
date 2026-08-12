# JAX Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `jax.Array`

A device-backed immutable array value. The critical boundary is: Host conversion and device transfer are explicit boundaries.

## `tracer`

A symbolic value observed while JAX traces a function. The critical boundary is: Python conversion or data-dependent Python control flow is invalid.

## `transformation`

jit, grad, vmap, pmap, or another program transform. The critical boundary is: The function must be pure over compatible pytrees and shapes.

## `PRNG key`

An explicit immutable random-state token. The critical boundary is: Split or fold in unique identities; reusing a key repeats randomness.

## `pytree`

A nested structure of leaves with registered container shape. The critical boundary is: Treedef and leaf shapes/dtypes form part of compiled contracts.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
