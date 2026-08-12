# SQLGlot AST and dialect model

## Parse and generate

A dialect supplies parser/tokenizer and generator rules. Parsing without a
known source dialect uses SQLGlot's permissive superset, which can interpret
vendor syntax differently from the originating engine. Generation without a
target dialect emits the generic dialect, not necessarily runnable target SQL.

`parse` returns all statement roots. `parse_one` is for a contract that expects
one expression. Each root and child is an `Expression` whose semantic children
live in named arguments; lists of expressions are distinct from scalar child
arguments.

## Names, values, and ownership

Identifiers represent names and carry quoting/case semantics. Literals
represent SQL values. Placeholders represent executor-bound values. Do not
parse untrusted input into an AST when it should remain a bound value.

Treat an AST as caller-owned unless the function contract transfers ownership.
Some fluent APIs mutate. Copy before modification when callers may reuse or
compare the original, and test parent/child relationships after replacement.

## Syntax tree versus resolved query

Local traversal can locate a `Column`, `Table`, `Func`, or statement class. It
cannot alone resolve aliases, CTE shadowing, correlated references, stars, or
type-dependent overloads. Scope analysis and qualification add resolution, and
often require a real schema mapping. Unknown catalog facts must remain unknown.
