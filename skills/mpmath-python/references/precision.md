# Numbers and precision

`mp.dps` is decimal working precision and `mp.prec` is binary precision. They
describe arithmetic context, not guaranteed final accuracy. Use scoped
`workdps`/`workprec` so a helper does not alter unrelated code.

Construct exact integers directly, exact rational input as a quotient formed in
the mpmath context, and decimal input from strings. Converting an existing
Python float preserves its binary approximation. When source measurements have
limited accuracy, record that limit rather than displaying extra digits.

`mpf` construction rounds at the current precision, so parse decimal strings
inside the intended working context. `workdps(n)` sets total decimal precision;
`extradps(n)` adds digits to the current context.

Leaving a context restores its settings but does not round an already-created
value. Apply unary plus inside an explicit output context when rounding is the
policy, or serialize with a stated digit count. Define whether the boundary
returns such a rounded value, a string, or a result from an isolated context.

Real and complex functions have branches. State whether complex output is
allowed, what branch is intended, and how points on/near cuts are tested.
