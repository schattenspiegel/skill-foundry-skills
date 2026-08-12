# asyncio Python decision guide

        ## Ordered decisions

        1. Use `TaskGroup` when sibling work should fail and clean up as one unit; use `gather` only when its different failure semantics are intentional.
2. Bound concurrency at the resource operation, not only at task creation, and preserve input ordering explicitly when the result contract requires it.
3. Re-raise `CancelledError` after local cleanup; do not convert cancellation into an ordinary failure or successful result.
4. Use a bounded queue when producers can outpace consumers; pair `put`, `task_done`, `join`, and worker shutdown deliberately.
5. Move blocking callables through `asyncio.to_thread`; state that cancelling the await does not forcibly terminate the underlying thread.
6. Inject clocks, events, and test doubles; do not verify concurrency with long sleeps or wall-clock races.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
