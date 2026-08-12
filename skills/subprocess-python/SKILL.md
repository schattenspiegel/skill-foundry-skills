---
        name: subprocess-python
        description: >-
          Use for writing, reviewing, debugging, or testing Python subprocess and process-management code, including argv, environments, pipes, timeouts, return codes, streaming, and termination. Do not use for asyncio-only task scheduling, invoking an already documented CLI, or shell-script authoring.
        argument-hint: "[subprocess Python task, code, contract, or failure]"
        ---

        # subprocess Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `argv` | A sequence passed directly to an executable. | It is not shell syntax when shell is false. |
| `CompletedProcess` | A finished command with status and captured streams. | check_returncode converts status into failure. |
| `Popen` | A live child-process handle and pipe owner. | Every opened pipe and process requires bounded completion. |
| `environment` | The child's key/value process environment. | Choose inheritance, allowlist, or explicit overrides deliberately. |
| `pipe` | A bounded OS byte stream. | Use communicate or concurrent draining to avoid deadlock. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Define executable, argv elements, stdin/stdout protocol, environment, and accepted exit codes.
2. Choose run or Popen from the required lifecycle.
3. Apply explicit timeout, capture/stream, encoding, and check behavior.
4. Close input and drain output before reaping the child.
5. Test quoted-looking data, nonzero exit, timeout, large output, and environment isolation.

        ## Decision rules

        - Pass an argv list with `shell=False` for ordinary commands; invoke a shell only when shell language is the intended input.
- Set text encoding explicitly for text protocols and keep bytes for byte protocols.
- Use `run` for bounded one-shot commands and `Popen` only when streaming, interaction, or lifecycle control requires it.
- Use `communicate` for paired pipes; do not wait before draining captured output.
- Define timeout aftermath and process-tree ownership; killing one process does not universally kill its descendants.
- Do not place secrets in argv when process listings or logs can expose them; prefer stdin or a protected file descriptor when supported.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `subprocess.safe-argv-json` and `subprocess.verify-argv-boundary`: execute untrusted-looking values as argv data.
- `subprocess.stdin-text-protocol` and `subprocess.verify-stdin-secret`: send a secret-like payload over stdin with bounded completion.
- `subprocess.communicate-dual-pipe` and `subprocess.verify-large-pipes`: drain stdout and stderr without pipe deadlock.

        Recipes are anchors, not blind templates. Preserve their named invariants and
        adapt types and names only after inspecting the actual boundary.

        ## Verification contract

        - Test observable behavior, not the presence of API tokens.
        - Exercise empty, singleton, malformed, and failure inputs when the operation
          accepts them.
        - Assert shape, dtype or type, ordering, ownership, and error semantics where
          they are part of the contract.
        - Keep external I/O deterministic with injected clocks, transports, processes,
          files, random state, or test doubles.
        - Run the narrow test first, then the relevant project suite. Do not declare
          completion when warnings, background failures, convergence flags, or cleanup
          errors remain unexplained.

        Use [the verification matrix](references/verification.md) for completion checks.

        ## Failure routing and adaptation

        Classify a failure before changing code: input-contract failures require a
        precise rejection; environment or version failures require inspection; execution
        failures require lifecycle, convergence, or cleanup evidence; invariant failures
        require a semantic correction. Do not relax a check, coerce a value, broaden a
        failure handler, or materialize data merely to make the symptom disappear.

        When adapting a recipe:

        1. Match its objects, ownership, execution timing, and output contract to the task.
        2. Preserve every branch condition and completion check while changing domain names.
        3. Add the project's real empty, malformed, duplicate, cancellation, precision, or
           boundary case before removing any guard.
        4. If the installed API differs, inspect the signature and primary documentation,
           then update implementation, test, and authoring evidence together.

        ## Version grounding

        Inspect the installed package and signature when editing an existing project.
        Treat examples here as verified anchors for the version recorded by the Foundry,
        not as permission to overwrite a repository's compatibility policy. When current
        behavior differs, preserve the project target and update tests and authoring
        evidence together.

        ## Completion

        Complete the task only when the implementation preserves the declared object
        model, no accidental materialization or lifetime extension was introduced, all
        failures are surfaced at the correct boundary, and deterministic tests prove the
        critical behavior. Report any environment or version fact that could not be
        verified.
