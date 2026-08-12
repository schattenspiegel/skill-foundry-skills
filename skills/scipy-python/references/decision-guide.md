# SciPy Python decision guide

        ## Ordered decisions

        1. Choose a solver from smoothness, bounds, derivative availability, sparsity, and bracketing information.
2. Check success or convergence flags and independently verify finite objective, residual, constraint, or reconstruction error.
3. Scale variables and residuals when magnitudes differ materially; report tolerances in the resulting units.
4. Provide analytic derivatives only when tested against finite differences or another independent check.
5. Prefer log-space survival and likelihood functions in tails where direct subtraction loses precision.
6. Use sparse formats deliberately and avoid accidental dense conversion in production-size paths.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
