# Verification and grounding

Primary sources inspected 2026-08-12:

- <https://mpmath.org/doc/current/>
- <https://mpmath.org/doc/current/basics.html>
- <https://mpmath.org/doc/current/calculus/optimization.html>
- <https://mpmath.org/doc/current/calculus/integration.html>

Current docs identify mpmath 1.3.0. Inspect `mpmath.__version__` and help for the
installed callable. Tests need string-versus-float construction, scoped context
restoration, cancellation, a multiple/failed root, singular or split integral,
complex branch points, precision doubling, and serialization. Use mathematical
residuals/tolerances; do not compare formatted strings except at an output API.
