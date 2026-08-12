# SQLGlot version and API grounding

SQLGlot releases frequently, and its documented versioning permits
backward-incompatible changes in minor releases. Inspect the project lock and
installed package before using node argument names, optimizer helpers, scope
APIs, dialect options, or generator flags.

From the installed skill directory run:

```text
python scripts/inspect_sqlglot.py sqlglot.parse_one sqlglot.transpile sqlglot.Expression.transform
```

The helper reports the installed distribution/module versions, supported
dialect names, and inspectable signatures. Where signatures are generic, use
the installed docstring and a minimal parse-transform-generate probe.

Pin or test exact SQLGlot output only when formatting is itself the contract.
For semantic transformations, assert AST properties and target execution rather
than brittle generated whitespace or quote style.
