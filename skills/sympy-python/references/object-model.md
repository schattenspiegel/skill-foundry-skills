# Expressions, domains, and assumptions

Expressions are immutable trees of `Basic` subclasses. `expr.func` and
`expr.args` describe construction; do not mutate internals. Canonical internal
ordering is not a user-facing derivation order.

Symbols with the same printed name but different assumptions are distinct
objects. Declare facts such as `real=True`, `positive=True`, or `integer=True`
when mathematically known; do not add assumptions merely to force a preferred
answer. Query assumptions with the supported predicates and handle unknown.

Use exact numeric atoms (`Integer`, `Rational`, algebraic numbers) for symbolic
work. `Float` carries finite precision. `evalf(n)` targets decimal digits but
cannot restore exact information already lost at construction.

`Eq` and inequality objects represent propositions. Sets represent domains and
solution sets, including intervals, unions, complements, images, and
`ConditionSet`. Preserve them when the answer is not a finite list.

For polynomials, generator choice and coefficient domain affect factorization,
division, roots, and algorithms. Use `Poly` when those semantics matter. For
matrices, distinguish a concrete matrix of expressions from an abstract matrix
expression and verify shapes.
