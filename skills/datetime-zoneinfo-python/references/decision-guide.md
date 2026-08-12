# datetime and zoneinfo Python decision guide

        ## Ordered decisions

        1. Use aware UTC datetimes for instants and named zones for user-facing civil time; never compare aware and naive values.
2. Validate local wall times by round-tripping through UTC; require an explicit fold when both occurrences are valid.
3. Add calendar recurrences in local date/time space, then resolve each occurrence; do not add 24 hours to preserve a local appointment.
4. Define interval inclusion and normalize both endpoints and probes to UTC before comparison.
5. Parse only accepted formats and offsets; do not attach `tzinfo` to reinterpret an instant from another zone.
6. Inject `now` into business logic and test transition dates with the same tzdata policy as production.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
