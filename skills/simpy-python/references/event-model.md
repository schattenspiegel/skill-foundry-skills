# Event and process model

An event progresses from not triggered to triggered, then processed. A process
waits by yielding an event; a process itself is an event that succeeds with the
generator's return value or fails with its exception. `env.process()` schedules
the generator. `yield env.process(child(...))` waits for the child; calling
`child(...)` alone creates only a generator.

Conditions return information about completed constituent events. For a race,
handle ties and cleanup: several events can trigger at the same simulation time.
An interrupt is delivered as an exception at the process's current yield point.
Use `try/finally` or a request context to preserve ownership invariants.

The environment's `now` is a model number in the chosen time unit. Never mix it
silently with `datetime`, `time.sleep`, or CPU duration. Convert external times
at the boundary and document origin, unit, and inclusivity.

Use a deterministic trace for debugging: entity, event type, simulated time,
and stable identifiers. Logging every scheduler callback can change memory and
wall-clock cost, so monitoring must not alter semantic state.
