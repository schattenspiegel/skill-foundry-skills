# pytest and Hypothesis Integration verification matrix

        | Scenario | Required evidence | Recipe |
        |---|---|---|
        | `fixture-factory-per-example` | success + edge/failure path | `integration.verify-example-isolation` |
| `parametrize-generated-composition` | success + edge/failure path | `integration.verify-collected-cross-product` |
| `named-ci-profile-and-regression` | success + edge/failure path | `integration.verify-profile-and-example` |

        ## Evidence order

        1. Compile or import the artifact in the pinned environment.
        2. Run behavioral tests that call the target path.
        3. Assert cleanup, ordering, shape/type, warnings, and failure behavior.
        4. Use source inspection only to forbid a dangerous shortcut that behavior alone
           cannot distinguish.
        5. Run integration or project regression tests after the narrow contract passes.

        Do not treat mock evaluation, a successful import, or code-token presence as
        evidence that the implementation works in GitHub Copilot or the target model.
