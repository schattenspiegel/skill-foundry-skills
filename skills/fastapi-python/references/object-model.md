# FastAPI Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `FastAPI app`

The ASGI application and route/dependency registry. The critical boundary is: Create configuration and resources at an explicit composition boundary.

## `path operation`

A request-method and path contract. The critical boundary is: Its parameters and response model are public API semantics.

## `dependency`

A request or application-scoped provider graph. The critical boundary is: Yield dependencies own teardown after the response lifecycle.

## `lifespan`

One startup/shutdown context around the application. The critical boundary is: Clients must enter it in tests to observe initialized resources.

## `response model`

The validated and serialized public output schema. The critical boundary is: Use it to filter internal fields rather than returning storage objects unchecked.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
