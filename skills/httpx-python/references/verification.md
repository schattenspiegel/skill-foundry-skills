# HTTPX Python verification matrix

        | Scenario | Required evidence | Recipe |
        |---|---|---|
        | `borrowed-client-json` | success + edge/failure path | `httpx.verify-request-domain-contract` |
| `streaming-download` | success + edge/failure path | `httpx.verify-stream-cleanup` |
| `explicit-client-policy` | success + edge/failure path | `httpx.verify-timeout-limit-policy` |

        ## Evidence order

        1. Compile or import the artifact in the pinned environment.
        2. Run behavioral tests that call the target path.
        3. Assert cleanup, ordering, shape/type, warnings, and failure behavior.
        4. Use source inspection only to forbid a dangerous shortcut that behavior alone
           cannot distinguish.
        5. Run integration or project regression tests after the narrow contract passes.

        Do not treat mock evaluation, a successful import, or code-token presence as
        evidence that the implementation works in GitHub Copilot or the target model.
