# scikit-learn Python decision guide

        ## Ordered decisions

        1. Place every data-dependent preprocessing step inside a Pipeline or ColumnTransformer before cross-validation.
2. Choose KFold, StratifiedKFold, GroupKFold, or a time-ordered splitter from the sampling process; random splitting is not a neutral default.
3. Keep the untouched test set outside model selection and threshold tuning; report both selection and final evaluation procedures.
4. Set random_state on stochastic estimators and splitters, but do not confuse repeatability with uncertainty estimation.
5. Use task-appropriate metrics and state positive class, averaging, sample weights, and threshold policy.
6. Validate feature order, names, dtypes, missing-value handling, and learned-version compatibility at prediction boundaries.

        ## Unknown path

        If the target version, shape, dtype, ownership, clock, randomness, execution
        host, or failure policy is unknown, inspect it before editing code. If inspection
        is impossible, expose the uncertainty through an explicit parameter or guarded
        failure. Do not guess a convenient default when it can change correctness.

        ## Shortcut rejection

        Reject a requested shortcut when it breaks a named invariant, while preserving
        the user's legitimate outcome. Explain the smallest required correction and prove
        it with the nearest deterministic check.
