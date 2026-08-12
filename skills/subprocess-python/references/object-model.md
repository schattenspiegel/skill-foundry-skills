# subprocess Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `argv`

A sequence passed directly to an executable. The critical boundary is: It is not shell syntax when shell is false.

## `CompletedProcess`

A finished command with status and captured streams. The critical boundary is: check_returncode converts status into failure.

## `Popen`

A live child-process handle and pipe owner. The critical boundary is: Every opened pipe and process requires bounded completion.

## `environment`

The child's key/value process environment. The critical boundary is: Choose inheritance, allowlist, or explicit overrides deliberately.

## `pipe`

A bounded OS byte stream. The critical boundary is: Use communicate or concurrent draining to avoid deadlock.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
