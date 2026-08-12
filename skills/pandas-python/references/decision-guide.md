# pandas Python decision guide

        ## Ordered decisions

        1. Use `.loc` for labels and `.iloc` for positions; never infer which one integer-looking labels mean.
2. Treat binary operations as label-aligned; use arrays only when positional semantics are explicitly required.
3. Declare join keys, expected cardinality, null-key policy, suffixes, and row-order contract; use `validate` when known.
4. Use one assignment operation such as `.loc[...] = ...` and rely on Copy-on-Write semantics; do not chain indexers.
5. Choose nullable dtypes deliberately and test missing values without equating `NA`, `NaN`, and `None` in every context.
6. Prefer vectorized/grouped operations; use apply only when its input/output shape and dtype are explicit and tested.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
