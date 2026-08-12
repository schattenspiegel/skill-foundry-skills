# Resources, time, and experiments

## Pick the constrained thing

- `Resource(capacity=n)`: at most `n` concurrent users.
- `PriorityResource`: same ownership model, priority-ordered wait queue.
- `PreemptiveResource`: higher-priority requests may interrupt current users.
- `Container(capacity, init)`: aggregate level with blocking `put`/`get`.
- `Store(capacity)`: item queue; `FilterStore` selects matching objects;
  `PriorityStore` orders items.

Every request/get/put returns an event. Yield it before assuming acquisition or
state change. Define abandonment/timeout races and release/cancel outstanding
requests that lose.

## Measurement

Choose entity-based metrics (wait per completed customer), time-based metrics
(resource utilization), or state-at-time metrics deliberately. For a time
average, accumulate `previous_value * (now - previous_time)` at every change.
For warm-up deletion, decide how entities spanning the cutoff contribute.

## Replications

Keep model construction in a function that accepts configuration and seed and
returns structured results. A replication gets a fresh `Environment`, domain
state, resources, and RNG. Validate invariants per run, then summarize estimates
and intervals across runs. Increasing simulated horizon is not interchangeable
with independent replications when initial conditions or autocorrelation matter.
