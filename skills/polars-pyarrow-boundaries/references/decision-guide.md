# Polars and PyArrow Boundaries decision guide

        ## Ordered decisions

        1. Declare names, order, Arrow and Polars dtypes, nullability, timezone, precision, nested shape, and metadata requirements before conversion.
2. Use `pl.from_arrow` and `.to_arrow()` as explicit boundaries, then compare schemas and representative null/value behavior.
3. Treat zero-copy as an optimization requiring compatible representation, stable ownership, and buffer-level evidence; correctness must not depend on it.
4. Preserve timezone and timestamp unit deliberately; Python-object conversion can truncate nanoseconds and erase Arrow distinctions.
5. Decide whether dictionary encoding and chunk boundaries are semantic, performance-only, or allowed to normalize.
6. Version-ground unstable or evolving nested and extension-type behavior against both installed libraries.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
