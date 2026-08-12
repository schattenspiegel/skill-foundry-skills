# HTTPX Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `Client`

A sync connection pool and configuration owner. The critical boundary is: Create at an application/session boundary, not per request.

## `AsyncClient`

An async connection pool tied to async lifecycle. The critical boundary is: Close it in the same event-loop ownership scope.

## `Request/Response`

Protocol messages with headers, content, and status. The critical boundary is: Streaming bodies hold resources until consumed or closed.

## `Transport`

The I/O implementation below client policy. The critical boundary is: MockTransport replaces network behavior without patching client methods.

## `Timeout/Limits`

Separate connect/read/write/pool budgets and pool capacity. The critical boundary is: They are not an end-to-end retry deadline.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
