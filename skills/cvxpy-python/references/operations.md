# Modeling, solving, and validation

## Repeated models

Use Parameters for data that changes between solves. Set declared signs/domains,
assign compatible values, and check `problem.is_dcp(dpp=True)` before claiming
DPP caching. Reconstruct the Problem if objective or constraint structure
changes.

## Solvers and status

Query `cp.installed_solvers()`. Match continuous LP/QP/conic, mixed-integer, or
special problem structure to a capable solver. Handle `OPTIMAL`,
`OPTIMAL_INACCURATE`, `INFEASIBLE`, `UNBOUNDED`, their inaccurate variants, and
ambiguous statuses according to the installed release. Record solver name,
options, status, objective, iterations, and residual evidence for diagnostics.

## Independent checks

After solving, compute constraint residuals from numeric inputs and copied
variable values without trusting only solver status. Check bounds, equalities,
cone/PSD conditions, and integrality at declared tolerances. Recompute the
objective. For sensitive work, perturb data, compare solvers, and inspect dual
or KKT conditions where valid.

Vectorize constraints and atoms instead of building huge Python loops when a
matrix formulation preserves the mathematics. Measure canonicalization and
solve time separately.
