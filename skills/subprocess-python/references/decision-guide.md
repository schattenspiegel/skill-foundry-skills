# subprocess Python decision guide

        ## Ordered decisions

        1. Pass an argv list with `shell=False` for ordinary commands; invoke a shell only when shell language is the intended input.
2. Set text encoding explicitly for text protocols and keep bytes for byte protocols.
3. Use `run` for bounded one-shot commands and `Popen` only when streaming, interaction, or lifecycle control requires it.
4. Use `communicate` for paired pipes; do not wait before draining captured output.
5. Define timeout aftermath and process-tree ownership; killing one process does not universally kill its descendants.
6. Do not place secrets in argv when process listings or logs can expose them; prefer stdin or a protected file descriptor when supported.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
