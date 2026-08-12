# Testing Rich output

## Stable harness

```python
from io import StringIO

from rich.console import Console


def test_render_jobs():
    target = StringIO()
    console = Console(
        file=target,
        width=60,
        color_system=None,
        force_terminal=False,
    )
    render_jobs(console, [{"id": 7, "state": "ready", "owner": "[ops]"}])
    output = target.getvalue()
    assert "7" in output
    assert "ready" in output
    assert "[ops]" in output
    assert "\x1b[" not in output
```

Use a fresh console per test. Fix width and color behavior rather than inheriting
the developer's TTY. Assert semantic fields and relative ordering. Add a narrow
width case for tables and a no-record case for empty state.

Test ANSI/style only when it is a public requirement; then force a known color
system and assert a small specific sequence or inspect rendered segments. Full
snapshots are brittle across Rich versions, terminal width, Unicode support,
and table layout changes.

For progress/live code, inject a console and deterministic time source where
the installed API supports it. Prefer testing state updates separately from the
animation. At minimum prove non-TTY execution terminates, leaves no control
codes in a plain target, and preserves errors.
