# pytest and Hypothesis Integration decision guide

        ## Ordered decisions

        1. Assume a function-scoped pytest fixture is shared across all Hypothesis examples for one item; use a fixture-provided factory or explicit reset for per-example state.
2. Keep `@pytest.mark.parametrize` outside `@given` conceptually: each pytest parameter is one item with its own generated example stream.
3. Use `@example` for known regressions and generated strategies for the general invariant; do not replace either with the other.
4. Register named settings profiles with explicit max_examples, deadline, and database policy; do not suppress health checks without a documented cause.
5. Do not catch Hypothesis assertion failures or share mutable globals, real network, or wall-clock state across examples.
6. Run pytest through the pinned environment so plugin discovery, profile, and Hypothesis version match CI.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
