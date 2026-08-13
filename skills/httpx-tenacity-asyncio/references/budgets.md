# Time budgets

Treat connect, pool, write, and read timeouts as inactivity budgets for individual
phases. They do not by themselves cap a multi-attempt operation. Put a deadline around
the retry loop and choose attempt limits/backoff that fit inside it.

When a deadline is inherited from a caller, pass the remaining budget down rather than
starting a fresh full budget at every layer. Test with a deterministic fake transport
and injected waits; do not make unit tests sleep in wall-clock time.
