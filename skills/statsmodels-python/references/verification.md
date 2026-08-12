# statsmodels Python verification matrix

        | Scenario | Required evidence | Recipe |
        |---|---|---|
        | `formula-ols-hc3` | success + edge/failure path | `statsmodels.verify-design-and-covariance` |
| `mean-and-observation-intervals` | success + edge/failure path | `statsmodels.verify-interval-semantics` |
| `ordered-hac-regression` | success + edge/failure path | `statsmodels.verify-time-and-lag-contract` |

        ## Evidence order

        1. Compile or import the artifact in the pinned environment.
        2. Run behavioral tests that call the target path.
        3. Assert cleanup, ordering, shape/type, warnings, and failure behavior.
        4. Use source inspection only to forbid a dangerous shortcut that behavior alone
           cannot distinguish.
        5. Run integration or project regression tests after the narrow contract passes.

        Do not treat mock evaluation, a successful import, or code-token presence as
        evidence that the implementation works in GitHub Copilot or the target model.
