# SQLGlot operation map

## Parse and errors

- Use `parse_one` for a proven single-expression boundary and `parse` for
  scripts. Catch `ParseError` only to add stable context; retain structured
  diagnostics.
- Validate statement/root classes immediately after parsing. An AST is not an
  authorization decision by itself.

## Inspect and analyze

- Use `find`/`find_all` for syntactic presence and expression properties for
  local semantics.
- Use scopes and qualification for resolved sources and columns. Supply schema
  for star expansion and type-sensitive analysis.
- Use lineage helpers only after defining how aliases, stars, and unknown
  schemas are handled.

## Build and transform

- Prefer `sqlglot.exp` builders/nodes over hand-concatenated SQL.
- Use `transform` for recursive rewrites and explicit replace/set operations for
  local changes. Copy if mutation is not part of the public contract.
- Avoid manually ordering individual optimizer rules; use supported composed
  entry points and test the canonical form.

## Generate and transpile

- Generate with `.sql(dialect=...)` or `transpile(read=..., write=...)`.
- Raise on unsupported constructs for correctness-critical work.
- Reparse output with the target dialect. Execute equivalence fixtures in the
  actual source/target engines for claims beyond syntax.
