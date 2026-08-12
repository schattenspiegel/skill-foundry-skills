# API grounding

Load this reference when an exact parameter, dtype, warning, engine, exception, or capability can vary by Polars version.

## Evidence order

1. Inspect the target project's `pyproject.toml`, lockfile, requirements, and tests.
2. Inspect the active environment.
3. Inspect the exact installed object with `inspect.signature`, `help`, or its docstring.
4. Use current official Polars versioned documentation when the project supports more than the active version.
5. Add a compatibility test for every supported branch.

Do not perform version archaeology for stable expression semantics already covered by project tests. Do not implement against newest documentation when the target lockfile says otherwise.

## Inspection helper

From the installed skill directory run:

```text
python scripts/inspect_polars.py
```

The helper writes one JSON object containing Python and Polars versions plus an
`apis` entry for each drift-prone operation. Every entry reports `available`
and either its inspected `signature` or `null`. Missing APIs therefore remain
diagnostic evidence instead of crashing the helper. Exit `0` means evidence
was collected. Exit `2` means Polars is not importable. Other nonzero exits are
helper failures and must be reported.

For focused lookup, pass one or more dotted paths. Paths normally resolve from
the top-level `polars` module; `selectors.*` and `testing.*` resolve from those
submodules:

```text
python scripts/inspect_polars.py DataFrame.select Series.str selectors.numeric
```

An unknown path is returned with `"available": false`; it does not make the
whole probe fail. A missing signature does not mean a property or namespace is
absent—read its `available` field and inspect the returned object or current
official page when Python introspection cannot expose a signature.

Useful direct inspection:

```python
import inspect
import polars as pl

print(pl.__version__)
print(inspect.signature(pl.LazyFrame.join))
print(inspect.signature(pl.LazyFrame.collect))
```

If the supported version range contains different signatures, use a narrow compatibility branch or the oldest supported common API. Never suppress deprecation warnings merely to keep an obsolete call.

## Drift triggers

Re-check exact behavior when code uses join keyword names, scan schema/index
parameters, streaming engines, sinks or batch consumers, lazy pivot,
`join_where`, temporal grouping, explode options, UDF arguments, concat modes,
testing tolerances, unstable APIs, or deprecation warnings. Query-plan text is
diagnostic output, not a durable public contract; pin plan assertions to a
tested project version.
