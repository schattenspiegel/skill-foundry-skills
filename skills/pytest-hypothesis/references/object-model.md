# pytest and Hypothesis Integration object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `pytest item`

One collected test function and parameter instance. The critical boundary is: Hypothesis executes many generated examples inside that item.

## `fixture value`

State created according to pytest fixture scope. The critical boundary is: Function-scoped fixtures are not recreated for every generated example.

## `generated example`

One Hypothesis input and shrink candidate. The critical boundary is: It must begin from equivalent clean state.

## `settings profile`

Named budgets and health-check policy. The critical boundary is: CI and local profiles should be selected explicitly and recorded.

## `failure database`

Stored examples that replay previous failures. The critical boundary is: It complements deterministic seeds and explicit regression examples.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
