# Algorithms and validation

## Root finding

Choose starts from domain knowledge; brackets or multiple starts may imply a
different solver. Verify residual at higher precision and confirm the intended
root, especially with multiple roots. Treat convergence exceptions as outcomes.

## Integration and sums

Split at discontinuities, singularities, and regime changes. Compare precision
and, for difficult cases, alternate quadrature or analytic identities. Infinite
and oscillatory integrals need methods suited to their structure.

## Linear algebra and special functions

For matrices, inspect condition and residual `A*x-b`; extra digits do not make a
singular system well-posed. Use native special functions and scaled/log forms
when available to avoid overflow/cancellation.

## Evidence pattern

Compute at `p` and `p + guard`, compare results under the target norm, and check
an independent residual or identity. Stop with an explicit failure if evidence
does not stabilize; do not return the last iterate as though it met the target.
