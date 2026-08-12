# pytest Python decision guide

        ## Ordered decisions

        1. Arrange state in explicit fixtures and release it with `yield` plus `finally`; teardown must work after assertion and setup failures.
2. Choose the narrowest fixture scope compatible with cost and isolation; never share mutable function expectations through session scope.
3. Patch the symbol in the module that looks it up, before the call under test, and prefer dependency injection for code you own.
4. Parametrize behaviorally distinct boundaries with readable IDs; do not mutate parameter values between items.
5. Assert exception type and meaningful fields or message fragments, and keep the call that must raise inside the raises block.
6. Block real network, clock, randomness, home-directory, and subprocess dependencies unless the test is explicitly an integration test.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
