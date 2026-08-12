# FastAPI Python decision guide

        ## Ordered decisions

        1. Separate transport models from domain and persistence objects; validate at the request boundary and filter at the response boundary.
2. Use dependencies for explicit resource and authorization contracts, with `yield` plus `finally` for owned cleanup.
3. Create long-lived pools and clients in lifespan and store only deliberate application state; do not construct them per request.
4. Use sync endpoints only for bounded blocking work that the host can thread; keep blocking calls out of async endpoints.
5. Map expected domain failures to explicit HTTP status and safe detail; let unexpected errors remain observable to logging and tests.
6. Test through TestClient or HTTPX ASGITransport with lifespan and dependency overrides scoped and restored.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
