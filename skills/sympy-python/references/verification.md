# Verification and grounding

Primary sources inspected 2026-08-12:

- <https://docs.sympy.org/latest/index.html>
- <https://docs.sympy.org/latest/tutorials/intro-tutorial/basic_operations.html>
- <https://docs.sympy.org/latest/guides/assumptions.html>
- <https://docs.sympy.org/latest/modules/solvers/solveset.html>

The documentation release is 1.14.0. Verify installed version and signatures.
Tests should cover exact rational versus float input, assumptions known/unknown,
structurally different equivalent expressions, removable singularities,
multiple/no/conditional solutions, real versus complex domains, and lambdified
array/numeric behavior. Assert mathematics and type/set contract separately
from printed formatting.
