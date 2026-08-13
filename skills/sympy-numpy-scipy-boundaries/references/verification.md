# Cross-boundary verification

Test symbolic identities before translation where possible. After translation, compare
values at regular points, near boundaries, and at randomized domain points. For
derivatives, compare the symbolic derivative with a carefully scaled finite-difference
or complex-step check when applicable.

For a solve, report the solution, residual norm, constraint violation, tolerance, and
initialization or bracket. Repeat with tighter tolerance or higher precision when the
result is sensitive. Preserve the symbolic expression and parameter values as evidence.
