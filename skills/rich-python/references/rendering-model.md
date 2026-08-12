# Rich rendering model

## Data to pixels/text

The pipeline is:

```text
domain values -> renderable tree -> Console options -> segments -> target stream
```

A renderable should describe meaning without reading global terminal state.
`Console` supplies width, height, color system, terminal/interactivity flags,
encoding, and stream. This separation makes rendering reusable and testable.

## Text trust boundary

Markup is a parser, not harmless decoration. Use trusted literal markup only
for developer-authored templates. For names, paths, exception messages, log
fields, or any user/external value:

- pass a `Text` instance;
- call `rich.markup.escape` before interpolation into trusted markup; or
- pass `markup=False` for a literal string.

Do not escape an entire string after embedding intended markup; separate styled
static text from literal dynamic text.

```python
from rich.text import Text

line = Text("Owner: ", style="bold")
line.append(owner_name)  # literal, even if it contains [red]
console.print(line)
```

## Custom renderables

Prefer composition from `Text`, `Table`, `Panel`, and `Group`. Implement
`__rich__` for a simple object that can return an existing renderable. Implement
`__rich_console__` only when streaming multiple segments/renderables or reacting
to console options is necessary. A custom renderable must handle narrow widths
and avoid mutation during rendering.

## Table contract

Columns represent stable fields; rows represent records. Decide alignment,
wrapping/overflow, missing-value text, ordering, and empty state. Convert values
to explicit strings or renderables. Do not let arbitrary dictionaries determine
column order across rows, and do not hide significant precision through visual
formatting without preserving the raw value elsewhere when required.
