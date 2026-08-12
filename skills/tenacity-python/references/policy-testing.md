# Retry policy and deterministic testing

## Budget equation

The total latency includes every attempt plus waits:

```text
sum(per-attempt duration) + sum(wait delays) + callback overhead
```

A stop-after-delay condition cannot interrupt a currently blocked call. Set the
transport/database timeout for each attempt below the caller's remaining
deadline. Account for lower layers that retry internally.

## Safe write branch

For a write, require one of:

- a server-supported idempotency key stable across attempts;
- an atomic upsert keyed by a stable business identifier;
- a transaction whose failed attempt is known to have rolled back; or
- a read-after-ambiguous-failure reconciliation protocol.

Otherwise propagate the first ambiguous failure. Never retry a sequence such as
`charge(); send_email()` as one unit merely because each function may fail.

## Test without sleeping

Inject `sleep=lambda _: None` into `Retrying` or replace the wait only in the
test-owned policy. Feed a deterministic sequence of results/exceptions. Assert:

- transient failures reach the expected success attempt;
- permanent failure executes exactly once;
- exhaustion raises the documented final exception (`reraise=True`) or
  `RetryError` when intentional;
- result retry does not retry a valid falsey result;
- callbacks receive the expected attempt numbers;
- the visible side effect occurs at most once.

Do not patch global time or sleep when controller injection can prove the same
behavior. Do not make production waits zero to satisfy tests.
