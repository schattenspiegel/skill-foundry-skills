# pytest Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `test item`

One collected executable test case. The critical boundary is: Parametrization creates distinct items and mutable parameters are not copied.

## `fixture`

A dependency-provided test context. The critical boundary is: Its scope controls cache lifetime, not safe mutation policy.

## `request`

The active item and fixture-resolution context. The critical boundary is: Dynamic fixture lookup hides dependencies and requires justification.

## `monkeypatch`

A reversible mutation ledger for one test scope. The critical boundary is: Patch the name looked up by code under test.

## `outcome`

Pass, fail, error, skip, or expected failure. The critical boundary is: Do not turn known defects into unconditional passing tests.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
