---
        name: fastapi-python
        description: >-
          Use for writing, reviewing, debugging, or testing Python FastAPI applications, including path operations, dependencies, Pydantic request/response models, lifespan, middleware, background tasks, exception handling, and ASGI tests. Do not use for outbound HTTPX clients or generic asyncio code with no ASGI boundary.
        argument-hint: "[FastAPI Python task, code, contract, or failure]"
        ---

        # FastAPI Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `FastAPI app` | The ASGI application and route/dependency registry. | Create configuration and resources at an explicit composition boundary. |
| `path operation` | A request-method and path contract. | Its parameters and response model are public API semantics. |
| `dependency` | A request or application-scoped provider graph. | Yield dependencies own teardown after the response lifecycle. |
| `lifespan` | One startup/shutdown context around the application. | Clients must enter it in tests to observe initialized resources. |
| `response model` | The validated and serialized public output schema. | Use it to filter internal fields rather than returning storage objects unchecked. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Define HTTP method/path, authentication, request schema, response schema, and error statuses.
2. Place domain work behind injected dependencies with explicit owners and teardown.
3. Choose sync or async execution from actual blocking behavior.
4. Filter and validate the response contract independently of internal models.
5. Test success, validation, authorization/domain errors, and lifespan cleanup.

        ## Decision rules

        - Separate transport models from domain and persistence objects; validate at the request boundary and filter at the response boundary.
- Use dependencies for explicit resource and authorization contracts, with `yield` plus `finally` for owned cleanup.
- Create long-lived pools and clients in lifespan and store only deliberate application state; do not construct them per request.
- Use sync endpoints only for bounded blocking work that the host can thread; keep blocking calls out of async endpoints.
- Map expected domain failures to explicit HTTP status and safe detail; let unexpected errors remain observable to logging and tests.
- Test through TestClient or HTTPX ASGITransport with lifespan and dependency overrides scoped and restored.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `fastapi.yield-dependency-owner` and `fastapi.verify-response-then-cleanup`: own and close a request-scoped resource after response completion.
- `fastapi.response-model-boundary` and `fastapi.verify-secret-field-exclusion`: prevent internal fields from escaping the API.
- `fastapi.lifespan-resource-owner` and `fastapi.verify-testclient-lifespan`: initialize and tear down application-scoped state.

        Recipes are anchors, not blind templates. Preserve their named invariants and
        adapt types and names only after inspecting the actual boundary.

        ## Verification contract

        - Test observable behavior, not the presence of API tokens.
        - Exercise empty, singleton, malformed, and failure inputs when the operation
          accepts them.
        - Assert shape, dtype or type, ordering, ownership, and error semantics where
          they are part of the contract.
        - Keep external I/O deterministic with injected clocks, transports, processes,
          files, random state, or test doubles.
        - Run the narrow test first, then the relevant project suite. Do not declare
          completion when warnings, background failures, convergence flags, or cleanup
          errors remain unexplained.

        Use [the verification matrix](references/verification.md) for completion checks.

        ## Failure routing and adaptation

        Classify a failure before changing code: input-contract failures require a
        precise rejection; environment or version failures require inspection; execution
        failures require lifecycle, convergence, or cleanup evidence; invariant failures
        require a semantic correction. Do not relax a check, coerce a value, broaden a
        failure handler, or materialize data merely to make the symptom disappear.

        When adapting a recipe:

        1. Match its objects, ownership, execution timing, and output contract to the task.
        2. Preserve every branch condition and completion check while changing domain names.
        3. Add the project's real empty, malformed, duplicate, cancellation, precision, or
           boundary case before removing any guard.
        4. If the installed API differs, inspect the signature and primary documentation,
           then update implementation, test, and authoring evidence together.

        ## Version grounding

        Inspect the installed package and signature when editing an existing project.
        Treat examples here as verified anchors for the version recorded by the Foundry,
        not as permission to overwrite a repository's compatibility policy. When current
        behavior differs, preserve the project target and update tests and authoring
        evidence together.

        ## Completion

        Complete the task only when the implementation preserves the declared object
        model, no accidental materialization or lifetime extension was introduced, all
        failures are surfaced at the correct boundary, and deterministic tests prove the
        critical behavior. Report any environment or version fact that could not be
        verified.
