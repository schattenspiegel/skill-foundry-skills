# Retry semantics

Retry connection establishment failures for operations that have not been sent.
Retry a response status only when the service contract declares it transient. Parse
`Retry-After` deliberately and cap it to the remaining deadline.

For POST or other side-effecting requests, require an idempotency key, conditional
write, transaction identifier, or server-side deduplication before retrying an
ambiguous outcome. Never use `retry_if_exception_type(Exception)` as a default: it can
retry programmer errors, validation failures, and cancellation-related conditions.
