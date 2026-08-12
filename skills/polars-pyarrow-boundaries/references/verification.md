# Polars and PyArrow Boundaries verification matrix

        | Scenario | Required evidence | Recipe |
        |---|---|---|
        | `timestamp-ns-timezone-roundtrip` | success + edge/failure path | `boundary.verify-nanosecond-timezone-values` |
| `chunked-nullable-table` | success + edge/failure path | `boundary.verify-nullability-and-values` |
| `dictionary-and-list-contract` | success + edge/failure path | `boundary.verify-decoded-and-nested-values` |

        ## Evidence order

        1. Compile or import the artifact in the pinned environment.
        2. Run behavioral tests that call the target path.
        3. Assert cleanup, ordering, shape/type, warnings, and failure behavior.
        4. Use source inspection only to forbid a dangerous shortcut that behavior alone
           cannot distinguish.
        5. Run integration or project regression tests after the narrow contract passes.

        Do not treat mock evaluation, a successful import, or code-token presence as
        evidence that the implementation works in GitHub Copilot or the target model.
