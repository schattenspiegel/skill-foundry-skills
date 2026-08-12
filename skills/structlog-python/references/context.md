# Context lifecycle

Load this reference when correlation fields must follow a request, task, job, or
nested operation.

At each independent request, task, or job boundary:

1. Clear context variables.
2. Bind only the correlation and identity fields needed for operations.
3. Add narrower fields with a returned bound logger or temporary context binding.
4. Reset or clear temporary context when leaving a nested scope.
5. Test two sequential units of work to prove the first unit's values do not leak.

## Scope decision

| Required lifetime | Mechanism |
|---|---|
| Current logger and descendants receiving it | `child = log.bind(...)` |
| Current execution context across independently obtained loggers | `bind_contextvars(...)` plus `merge_contextvars` |
| Lexically nested execution scope | `with bound_contextvars(...):` |
| One event only | keyword arguments on the log call |

`clear_contextvars()` and logger `.new()` affect different stores. Do not use one
as a substitute for the other.

Hybrid sync/async frameworks can isolate execution contexts differently. Add a
framework-level test that crosses the actual boundary. Test two sequential
requests and two concurrent requests with distinct IDs. Never log secrets,
authentication headers, full request bodies, configuration objects, or arbitrary
user payloads as context.
