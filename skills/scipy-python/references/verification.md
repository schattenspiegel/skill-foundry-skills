# SciPy Python verification matrix

        | Scenario | Required evidence | Recipe |
        |---|---|---|
        | `bounded-quadratic-minimize` | success + edge/failure path | `scipy.verify-optimality-status` |
| `bracketed-root` | success + edge/failure path | `scipy.verify-root-residual` |
| `sparse-linear-system` | success + edge/failure path | `scipy.verify-sparse-residual` |

        ## Evidence order

        1. Compile or import the artifact in the pinned environment.
        2. Run behavioral tests that call the target path.
        3. Assert cleanup, ordering, shape/type, warnings, and failure behavior.
        4. Use source inspection only to forbid a dangerous shortcut that behavior alone
           cannot distinguish.
        5. Run integration or project regression tests after the narrow contract passes.

        Do not treat mock evaluation, a successful import, or code-token presence as
        evidence that the implementation works in GitHub Copilot or the target model.
