# Async retry and observability

Use `async def` with `@retry` when one coroutine owns a stable policy. Use
`AsyncRetrying` for block iteration or injected policy. Never call synchronous
blocking I/O or `time.sleep` in an async attempt; Tenacity cannot make a blocking
client asynchronous.

Cancellation must escape. Catching/retrying a broad exception can delay task
cancellation depending on the runtime and exception hierarchy. Keep predicates
to domain-specific transient exceptions and test cancellation in the target
async framework.

## Callback event

A `before_sleep` callback is the natural retry event because it represents a
failed attempt that will be followed by another attempt. Derive fields from
`RetryCallState` defensively against the installed version:

- stable operation label, not raw callable repr;
- attempt number and elapsed seconds;
- exception class or safe result category;
- planned delay when available;
- request/correlation identifier supplied by the caller.

Do not log arguments, tokens, complete URLs with credentials, request bodies,
or full response content. Emit a separate terminal-failure metric at the caller
boundary; `before_sleep` cannot observe a failure that will not retry.
