# scikit-learn Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `estimator`

An object whose fit learns state from X and possibly y. The critical boundary is: Never fit it on validation or test information.

## `transformer`

An estimator that maps features through transform. The critical boundary is: Learn preprocessing inside the same training split as the estimator.

## `Pipeline`

An ordered preprocessing and final-estimator unit. The critical boundary is: Cross-validation clones and fits the whole unit per split.

## `splitter`

A policy yielding train/test indices. The critical boundary is: Choose it from independence, grouping, ordering, and class-balance assumptions.

## `scorer`

A maximization-oriented evaluation contract. The critical boundary is: Loss scorers may be negated; inspect sign and response method.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
