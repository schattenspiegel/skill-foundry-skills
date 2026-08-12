# HTTPX Python decision guide

        ## Ordered decisions

        1. Inject or application-scope a client so connection pooling survives related requests; a helper borrowing a client must not close it.
2. Set connect, read, write, and pool timeouts from the operation contract; do not disable all timeouts as a repair.
3. Use `stream` and consume or close the response inside its context when the body can exceed memory.
4. Call `raise_for_status` before trusting an HTTP success payload, then validate the domain payload separately.
5. Use MockTransport or ASGITransport in tests and assert outgoing request semantics without real network access.
6. Retry only replay-safe operations under an explicit budget; HTTPX transport retries do not replace domain retry decisions.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
