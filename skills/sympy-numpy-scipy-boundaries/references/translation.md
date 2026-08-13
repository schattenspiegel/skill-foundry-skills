# Symbolic-to-numeric translation

`lambdify` translates names and uses code generation; it is not a sandbox. Supply
symbols as an ordered tuple and select `modules` explicitly. Test the returned callable
on scalar and array inputs that the consumer will actually provide.

Translation can change semantics: integer inputs, complex branches, `Piecewise`, and
special functions may produce different dtypes, warnings, or unavailable operations.
Inspect generated behavior at domain boundaries instead of assuming algebraic
equivalence implies floating-point equivalence.
