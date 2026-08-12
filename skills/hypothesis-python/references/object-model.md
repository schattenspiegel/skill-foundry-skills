# Hypothesis Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `strategy`

A lazy description of a value space and shrink order. The critical boundary is: Construct valid structure rather than filtering broad invalid values.

## `example`

One generated or explicit test input. The critical boundary is: The test must be independent and deterministic for that input.

## `property`

An invariant checked across generated examples. The critical boundary is: It must be stronger than restating the implementation.

## `shrinker`

The search for a smaller failing example. The critical boundary is: Opaque setup, global state, and catching assertion failures obstruct it.

## `state machine`

Generated sequences of operations over mutable state. The critical boundary is: Use only when history affects validity or outcomes.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
