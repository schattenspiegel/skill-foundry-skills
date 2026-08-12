# Python typing decision guide

        ## Ordered decisions

        1. Model relationships, not decoration: use one type parameter when arguments and results must share a type.
2. Accept the narrowest structural Protocol needed by the function; return concrete capabilities the caller can rely on.
3. Use overloads only when argument forms determine return types and the implementation accepts every declared form.
4. Use ParamSpec to preserve callable parameters through decorators and `functools.wraps` to preserve runtime metadata.
5. Prefer precise unions plus narrowing over `Any`, unchecked casts, or broad ignores; scope unavoidable ignores to one diagnostic code.
6. Run the repository's configured checker and runtime tests because static correctness does not prove runtime validation.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
