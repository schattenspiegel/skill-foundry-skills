# Operations and numeric boundaries

## Targeted algebra

Select the requested representation:

- expand products/powers with `expand` variants;
- factor polynomial structure with `factor`/`factor_list`;
- combine/cancel rational functions with `together`/`cancel`;
- decompose rational functions with `apart`;
- collect coefficients by chosen generators with `collect`;
- use domain-specific trigonometric, power, logarithmic, or special-function
  rewrites only under valid assumptions.

For a rational-expression normalization that must preserve singularities,
first compute `combined = together(original)`, then extract
`fraction(combined)` and solve its denominator roots before returning
`cancel(combined)`. Extracting the denominator directly from an additive input
can miss the component denominators. No later transform can reconstruct domain
exclusions already erased when the original expression was constructed.

## Solving and calculus

Choose equation versus inequality and real/complex/integer domain explicitly.
Verify candidate solutions in the original relation, including denominator and
branch restrictions. For differentiation/integration/limits/series, preserve
the variable, point, direction, order, and convergence conditions.

## Numeric boundary

Use `evalf` for controlled high-precision evaluation of symbolic values. Use
`lambdify(arguments, expression, modules=...)` for repeated numeric calls;
define argument order, shapes, backend, dtype, complex behavior, and unsupported
function handling. Compare against exact or high-precision references at
regular and singular-nearby points. Never lambdify untrusted expressions.
