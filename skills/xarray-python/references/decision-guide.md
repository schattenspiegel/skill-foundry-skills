# Xarray Python decision guide

        ## Ordered decisions

        1. Name dimensions and coordinates from domain meaning; never rely on an axis number when labels are available.
2. Choose exact, inner, outer, left, or right alignment explicitly when combining independently sourced arrays.
3. Use `.sel` for coordinate labels and `.isel` for integer positions; state nearest/tolerance policy for approximate selection.
4. Define missing-data and weight normalization policy for reductions, especially when weights and values have different masks.
5. Preserve laziness across large chunked data and compute only at a tested consumer boundary.
6. Test dimension names, coordinate order/uniqueness, variable dtype, attrs/encoding, and calendar behavior where relevant.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
