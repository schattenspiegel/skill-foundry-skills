# Rigorous symbolic practice

Use this checklist when SymPy supports a mathematical derivation, proof audit,
solver, or high-consequence numerical result. It is a rigorous-computation
standard, not a description of any mathematician's private workflow.

## Frame and construct

1. **State the problem first.** Name the objects, hypotheses, domain, desired
   conclusion, and whether the task is discovery, verification, or numerical
   support.
2. **Separate discovery from proof.** Use computation to find patterns and
   counterexamples. Do not call a pattern or sampled identity a proof.
3. **Encode only justified assumptions.** Declare real, complex, positive,
   nonzero, integer, or finite facts when the mathematics supplies them. Do not
   add assumptions merely to force a preferred simplification.
4. **Treat every result as conditional.** Record branch conventions,
   exceptional values, excluded denominators, and convergence conditions.
5. **Construct exact inputs.** Prefer `Integer`, `Rational`, exact algebraic
   numbers, and strings for decimal input. A Python float has already rounded.
6. **Keep an audit trail.** Retain separate names for the original expression,
   each transformed form, and the claimed result.

## Transform and solve

7. **Choose a mathematical target form.** Use `factor`, `expand`, `cancel`,
   `together`, `apart`, `collect`, or a domain-specific transform because that
   representation serves the proof or consumer. `simplify()` is heuristic.
8. **Verify identities through a residual.** Transform `lhs - rhs` toward zero
   under the stated assumptions; structural `==` is not mathematical equality.
   A zero residual is still subject to the original domain exclusions.
9. **Record denominators before cancellation.** Combine additive fractions,
   extract roots of the uncancelled denominator, and only then cancel.
10. **Treat solver results as candidates.** Check finite candidates in the
    original equation. Preserve `ConditionSet`, families, and inconclusive
    checks rather than coercing them into a guessed list.
11. **Specify the solving domain.** Use set-valued solving when completeness
    matters. A complex solution set is not an answer to a real-only problem.
12. **Respect branches.** Audit logarithms, roots, inverse functions, and
    noninteger powers against principal-branch conventions and sign regions.

```python
import sympy as sp


def verified_real_solutions(
    equation: sp.Expr | sp.Equality,
    symbol: sp.Symbol,
) -> tuple[sp.Set, dict[sp.Expr, bool | None]]:
    residual = equation.lhs - equation.rhs if isinstance(equation, sp.Equality) else equation
    candidates = sp.solveset(equation, symbol, domain=sp.S.Reals)
    if not isinstance(candidates, sp.FiniteSet):
        return candidates, {}
    verdicts = {candidate: sp.checksol(residual, symbol, candidate) for candidate in candidates}
    verified = sp.FiniteSet(
        *(candidate for candidate, verdict in verdicts.items() if verdict is True)
    )
    return verified, verdicts
```

An empty verdict mapping means the exact set result was preserved rather than
pretending every non-finite result was individually checked. `None` means the
check was inconclusive.

## Test and falsify

13. **Sample strategically.** Include ordinary values, boundaries,
    near-singular points, large and small scales, both signs, and complex
    regions when relevant.
14. **Use precision deliberately.** Evaluate exact expressions at increasing
    precision and require stabilization. Machine-precision agreement is weak
    near cancellation or ill-conditioning.
15. **Distinguish unknown from false.** An unevaluated expression or an
    assumptions query returning `None` is incomplete inference.
16. **Exploit structure before brute force.** Reduce by symmetry, parity,
    scaling, invariants, substitutions, or dimension before expanding.
17. **Avoid unnecessary matrix inverses.** Solve `A*x=b` with the appropriate
    exact solver and verify the residual.
18. **Control expression growth.** Name subexpressions, factor intermediates,
    use common-subexpression elimination for generated code, and avoid global
    expansion without a size budget.
19. **Probe degeneracies.** Test zero, coincident parameters, rank loss,
    discriminant boundaries, and sign changes.
20. **Record convergence.** A closed form for a limit, integral, or sum is
    incomplete without the conditions under which it holds.

```python
solution = A.LUsolve(b)
residual = A * solution - b
if not all(value.equals(0) is True for value in residual):
    raise ArithmeticError("linear-system residual was not established as zero")
```

## Corroborate and communicate

21. **Use independent checks.** Corroborate by substitution, differentiation,
    coefficient comparison, a series, high-precision evaluation, or a second
    derivation; do not merely repeat the same transform.
22. **Use series locally.** Matching finitely many coefficients can refute a
    claim but does not establish a global identity by itself.
23. **Search for counterexamples deliberately.** Start with the smallest
    dimension, boundary cases, degenerate parameters, and nearly failed
    hypotheses.
24. **Turn repeated reasoning into assertions.** Package admissibility,
    residual, shape, and invariant checks in small tested helpers.
25. **Ground version-sensitive behavior.** Record `sp.__version__` and inspect
    installed signatures, solver return types, and printer/codegen behavior.
26. **Keep output auditable.** Prefer interpretable intermediate forms over an
    enormous equivalent expression.
27. **Do not cite tool output as the proof.** State the mathematical reason,
    theorem, or derivation; identify SymPy as computational support.
28. **Report the evidence class.** Use one of: symbolically established under
    stated assumptions, numerically supported, sampled only, conjectured, or
    unresolved.
29. **State why the conclusion holds.** Name the essential hypotheses and the
    cases where it fails.
30. **Stop at the evidence boundary.** If verification is inconclusive, return
    the unresolved condition or required next check instead of inventing
    certainty.

## Numerical root anchor

For a numerical root, parse a textual starting value at deliberate precision,
solve twice with increasing precision, compare the candidates, and evaluate the
original residual with `evalf(subs=...)`. Do not use ordinary `subs` as the
numerical residual check when cancellation can hide error.

```python
def stable_nsolve(expr, symbol, guess_text: str, digits: int = 30):
    if digits < 10:
        raise ValueError("digits must be at least 10")
    guess = sp.Float(guess_text, digits + 20)
    low = sp.nsolve(expr, symbol, guess, prec=digits + 20)
    high = sp.nsolve(expr, symbol, guess, prec=digits + 40)
    tolerance = sp.Integer(10) ** (-digits)
    if abs(low - high) > tolerance:
        raise ArithmeticError("root did not stabilize")
    residual = abs(expr.evalf(digits + 20, subs={symbol: high}))
    if residual > tolerance:
        raise ArithmeticError("root residual exceeds tolerance")
    return high.evalf(digits), residual
```
