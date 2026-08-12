# SciPy Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `objective/residual`

A callable encoding the numerical problem. The critical boundary is: Scale, domain, differentiability, and finite-value behavior determine solver suitability.

## `solver result`

An estimate plus convergence and diagnostic fields. The critical boundary is: A returned vector is not success until status and residual checks pass.

## `sparse matrix`

A structure storing selected entries and layout metadata. The critical boundary is: Choose CSR/CSC/COO from construction and operation patterns.

## `distribution`

A parameterized probability model with numerical methods. The critical boundary is: State parameterization and tail/log-space requirements.

## `tolerance`

An error scale in input, output, or residual space. The critical boundary is: Set it from the application scale, not an unexplained tiny literal.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
