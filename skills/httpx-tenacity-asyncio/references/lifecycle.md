# Lifecycle and concurrency

Create an `AsyncClient` in the owning application lifespan and close it once. Give
workers a borrowed client; they do not close it. Configure limits from expected
concurrency and the upstream's capacity.

Use structured concurrency (`TaskGroup` where appropriate) so failure and cancellation
ownership are visible. Limit admitted work with a semaphore or worker pool. Do not
spawn unbounded tasks merely because the connection pool queues them.

On cancellation, allow cleanup in `finally` blocks and re-raise. Do not shield an
entire request; shield only a small cleanup action whose completion is required.
