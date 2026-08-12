# Typer design and testing

## Error and stream contract

Classify failures before choosing output:

| Failure | Behavior |
|---|---|
| Parser/type/range/path failure | Let Typer render usage and a nonzero exit. |
| Cross-field user error | Raise `typer.BadParameter` or print a concise error to stderr then raise `typer.Exit(2)`. |
| Expected operational failure | Explain the actionable cause on stderr; use the documented nonzero code. |
| User cancellation | Exit with the command's cancellation code and perform no mutation. |
| Programmer defect | Do not blanket-catch it as a user error. Preserve diagnostic evidence. |

Machine-readable stdout must remain parseable. Put diagnostics and progress on
stderr. If the CLI promises JSON, emit exactly one documented JSON value or a
defined JSON-lines stream and keep Rich markup away from that stream.

## Side-effect boundary

Prompt and validate before the mutation. A destructive command should follow:

1. resolve exact targets;
2. reject invalid/ambiguous targets;
3. show a preview when required;
4. confirm unless an explicit non-interactive flag authorizes execution;
5. apply once;
6. verify or return failure.

A callback must not perform the mutation before command-specific validation.

## Canonical test matrix

```python
from typer.testing import CliRunner

from package.cli import app

runner = CliRunner()


def test_export_rejects_existing_output(tmp_path):
    source = tmp_path / "in.txt"
    output = tmp_path / "out.txt"
    source.write_text("x")
    output.write_text("old")

    result = runner.invoke(app, ["export", str(source), "-o", str(output)])

    assert result.exit_code != 0
    assert "--force" in result.output
    assert output.read_text() == "old"
```

Test at least:

- `--help`, command names, aliases, and required/default display;
- a representative successful invocation and exact side effect;
- parser rejection for invalid types and missing required values;
- command-level validation with a nonzero exit;
- prompt input using `input="...\n"` without leaking secrets;
- no-args and callback behavior for multi-command apps;
- the installed package entry point in a subprocess when packaging changes.

Do not assert only colorful whitespace or the full help snapshot unless exact
format is a compatibility promise. Prefer semantic substrings plus exit codes.
