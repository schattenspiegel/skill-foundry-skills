# Verification and API grounding

Primary docs inspected 2026-08-12:

- <https://numpy.org/doc/stable/user/basics>
- <https://numpy.org/doc/stable/user/basics.broadcasting.html>
- <https://numpy.org/doc/stable/user/basics.copies.html>
- <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>

The online stable manual currently reports NumPy 2.5. Inspect the project's
installed version and migration/release notes, especially across major-version
promotion, scalar, copy, string-dtype, and deprecated attribute behavior.

Tests should include scalar/0-D, `(n,)` versus `(n,1)`, singleton and empty axes,
noncontiguous transpose/slice, advanced indexing, shared-memory mutation,
integer overflow, float32 accumulation, `NaN`/infinities, object/ragged input,
and injected RNG repeatability. Assert with `numpy.testing` helpers plus explicit
shape, dtype, strides/ownership where part of the contract. Use residuals and
scale-based tolerances for numerical algorithms.
