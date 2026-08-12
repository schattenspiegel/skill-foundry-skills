# datetime and zoneinfo Python object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `instant`

One point on the UTC timeline. The critical boundary is: Represent it with an aware datetime and compare after UTC normalization.

## `wall time`

A calendar reading in a locality. The critical boundary is: It can be nonexistent or ambiguous at an offset transition.

## `ZoneInfo`

Rules for a named IANA time zone. The critical boundary is: It is not a fixed offset and requires available time-zone data.

## `fold`

The selected occurrence of an ambiguous wall time. The critical boundary is: It does not repair nonexistent times.

## `interval`

A start and end with an inclusion policy. The critical boundary is: Default to half-open only when the contract states it.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
