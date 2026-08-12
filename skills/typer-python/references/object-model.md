# Typer command object model

## Topology decision

Start from the user-visible invocation grammar, not decorators.

| Grammar | Structure |
|---|---|
| `tool INPUT [OPTIONS]` | One command; `typer.run` is acceptable for a truly small script, while an explicit app is easier to compose and test. |
| `tool create ...`, `tool delete ...` | One `Typer` app with peer commands. |
| `tool users create ...`, `tool jobs run ...` | Root app with independently defined sub-apps added by `add_typer`. |
| `tool [GLOBAL OPTIONS] COMMAND ...` | Root callback parses global state; command consumes typed `ctx.obj`. |

Adding a callback changes command topology. In particular, a single decorated
function can be promoted from the root invocation to a named subcommand. Lock
this with help and invocation tests before refactoring.

## Parsing lifecycle

1. The process resolves the packaging entry point.
2. Typer/Click identifies command path and parameters.
3. Eager callbacks and completion-sensitive paths may run.
4. Group callbacks run before the selected command.
5. The command adapter receives converted Python values.
6. The adapter calls domain logic and maps expected results/failures.
7. The process exits; context-managed resources close.

Do not open databases or mutate state at import time. Do not assume a parameter
callback runs only during a real command: shell completion can invoke it.

## Data flow

Command annotations describe terminal parsing, not the domain model. Convert
once at the edge:

```python
@app.command()
def create(config: Annotated[Path, typer.Option(exists=True)]) -> None:
    request = CreateRequest.from_file(config)
    result = create_resource(request)
    typer.echo(result.identifier)
```

The domain function should not import Typer or call `typer.echo`. This permits
ordinary unit tests and reuse from services or jobs.

## Context discipline

Use `ctx.obj` for values genuinely shared by commands in one invocation, such
as a loaded configuration or injected client. Initialize it once in the root
callback and type-check/narrow it at the command boundary. Use
`ctx.invoked_subcommand` only to distinguish root-only behavior from a selected
subcommand. Raw `ctx.args` is a compatibility escape hatch for deliberate
pass-through; it forfeits normal typed validation.
