# JAX Python decision guide

        ## Ordered decisions

        1. Keep transformed functions pure: return updated values and effects as data rather than mutating Python or global state.
2. Use JAX control-flow primitives for traced data-dependent loops and branches; Python control flow is only for static decisions.
3. Split keys before independent random uses and fold in stable step/device identities for reproducible parallel work.
4. Separate static configuration from dynamic arrays and avoid recompilation caused by changing shapes or Python objects.
5. Keep arrays on device through the compute region; block_until_ready when measuring execution rather than dispatch.
6. Check gradients against finite differences or a known derivative on small, smooth, nondegenerate inputs.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
