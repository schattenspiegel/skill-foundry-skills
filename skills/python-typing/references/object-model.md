# Python typing object model

        Select objects by semantic role, not by the shortest available syntax.

        ## `annotation`

Static information consumed by type checkers and tools. The critical boundary is: It normally performs no runtime validation.

## `Protocol`

A structural interface satisfied by compatible members. The critical boundary is: Mutable protocol attributes are invariant.

## `type parameter`

A relationship between input and output types. The critical boundary is: Use a bound for capabilities and constraints for a finite promoted family.

## `TypedDict`

A static mapping shape. The critical boundary is: It remains a dict at runtime and keys can have requiredness rules.

## `narrower`

A predicate that refines a value type. The critical boundary is: TypeIs narrows both branches only when its output type is assignable to input.

        ## Cross-object invariant

        Before composing objects, name who creates them, who may mutate them, when work
        executes, and who closes or finalizes them. A helper that borrows an object must
        not silently close, cache, materialize, or retain it.
