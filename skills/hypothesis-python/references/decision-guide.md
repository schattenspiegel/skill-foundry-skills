# Hypothesis Python decision guide

        ## Ordered decisions

        1. Derive strategies from the input contract and construct valid relationships directly with composite or flatmap strategies.
2. Assert semantic invariants, round trips, or agreement with an independent oracle; do not duplicate the implementation algorithm.
3. Avoid `.filter` and `assume` when a constructive strategy can express the domain and shrink better.
4. Keep generated tests free of shared mutable state, real network, wall clocks, and uncontrolled randomness.
5. Use a rule-based state machine only when operation sequences expose defects that single calls cannot.
6. Retain production regressions with `@example` while keeping the general property that found them.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
