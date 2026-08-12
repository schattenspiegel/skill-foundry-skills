# asyncio Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `coroutine`

A suspended computation created by calling an async function. The critical boundary is: It does not run until awaited or scheduled.

## `Task`

An event-loop-owned running coroutine with a result or exception. The critical boundary is: Keep a strong owner until completion.

## `TaskGroup`

A structured scope that owns sibling tasks. The critical boundary is: A non-cancellation failure cancels remaining siblings and exits with an exception group.

## `Queue`

A bounded handoff and backpressure point. The critical boundary is: Every accepted item requires exactly one task_done call.

## `timeout`

A cancellation scope transformed into TimeoutError at its boundary. The critical boundary is: Cleanup must remain cancellation-safe.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
