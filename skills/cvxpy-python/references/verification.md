# Verification and grounding

Primary sources inspected 2026-08-12:

- <https://www.cvxpy.org/tutorial/intro/index.html>
- <https://www.cvxpy.org/tutorial/dcp/>
- <https://www.cvxpy.org/tutorial/dpp/index.html>
- <https://www.cvxpy.org/tutorial/constraints/index.html>
- <https://www.cvxpy.org/tutorial/solvers/>

Before coding, print the installed CVXPY version and
`cvxpy.installed_solvers()`. Inspect atom and solve signatures for drift.

Tests need a hand-solvable feasible problem, an infeasible problem, an
unbounded problem, shape mismatch, prohibited chained comparison, DCP failure,
Parameter update, and solver-unavailable path. Validate numeric residuals and
objective, not exact floating output strings. Package absence means mock/static
foundry results are not CVXPY runtime evidence.
