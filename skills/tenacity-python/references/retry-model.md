# Tenacity retry state model

One logical invocation contains attempts. After an attempt, the retry predicate
examines its exception or result. If it is not retryable, the outcome returns or
raises immediately. If retryable, the stop strategy decides whether the budget
is exhausted. Otherwise callbacks run around a wait and the next attempt.

The first call is attempt 1. `stop_after_attempt(3)` permits at most three total
attempts, not three retries after the first call.

## Predicate composition

Use `retry_if_exception_type(SpecificTransientError)` for typed transient
failures. Combine alternatives with `|` only when either is independently
retryable; use `&` only when both predicates must hold. Result predicates must
not confuse an empty but valid result with a transient result.

Avoid message matching when a stable exception type/status is available.
Before retrying an HTTP status, follow the client's documented exception model
and exclude authentication, authorization, invalid request, and not-found
responses unless the domain explicitly says otherwise.

## Controller forms

Use a decorator for a stable reusable function policy. Use `Retrying` as a
callable when code selects a policy at runtime. Use its attempt context manager
when the safe retry unit is a block, but keep all state needed by a retried
result inside that attempt. With a result predicate and block iteration, set the
attempt's result as required by the installed API; otherwise the predicate may
see `None` rather than the computed value.

Use `retry_with(...)` only for a deliberate per-call policy override. Dynamic
policy should remain observable and tested, not spread as magic values at call
sites.
