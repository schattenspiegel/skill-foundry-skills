---
        name: python-typing
        description: >-
          Use for designing, reviewing, debugging, or testing Python static types, including Protocol, generics, variance, overloads, TypedDict, ParamSpec, TypeGuard/TypeIs, narrowing, and public typed APIs. Do not use for Pydantic runtime validation, JSON Schema, or adding annotations without a type contract.
        argument-hint: "[Python typing task, code, contract, or failure]"
        ---

        # Python typing

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `annotation` | Static information consumed by type checkers and tools. | It normally performs no runtime validation. |
| `Protocol` | A structural interface satisfied by compatible members. | Mutable protocol attributes are invariant. |
| `type parameter` | A relationship between input and output types. | Use a bound for capabilities and constraints for a finite promoted family. |
| `TypedDict` | A static mapping shape. | It remains a dict at runtime and keys can have requiredness rules. |
| `narrower` | A predicate that refines a value type. | TypeIs narrows both branches only when its output type is assignable to input. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Identify which values and capabilities vary and which relationships callers need.
2. Choose nominal class, Protocol, TypedDict, union, or generic parameter from runtime semantics.
3. Specify variance and mutability boundaries before exposing containers or callbacks.
4. Implement narrowing or overload bodies that agree with every declared signature.
5. Run mypy or Pyright at the project target plus runtime tests for annotation-dependent code.

        ## Decision rules

        - Model relationships, not decoration: use one type parameter when arguments and results must share a type.
- Accept the narrowest structural Protocol needed by the function; return concrete capabilities the caller can rely on.
- Use overloads only when argument forms determine return types and the implementation accepts every declared form.
- Use ParamSpec to preserve callable parameters through decorators and `functools.wraps` to preserve runtime metadata.
- Prefer precise unions plus narrowing over `Any`, unchecked casts, or broad ignores; scope unavoidable ignores to one diagnostic code.
- Run the repository's configured checker and runtime tests because static correctness does not prove runtime validation.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `typing.structural-reader` and `typing.verify-protocol-implementation`: accept a minimal structural dependency without inheritance.
- `typing.paramspec-decorator` and `typing.verify-decorator-signature`: preserve a wrapped callable signature and return type.
- `typing.typeis-payload` and `typing.verify-bidirectional-narrowing`: narrow an unknown mapping to a precise TypedDict.

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
