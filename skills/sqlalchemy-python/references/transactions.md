# Transactions and concurrency

Engine is a factory/pool; Connection and Session carry transaction state.
Autobegin can start a transaction on first use, so a read is not proof that no
transaction exists. Context managers establish deterministic commit/rollback
and release. Never share Session/AsyncSession across concurrent workers. For
tests, bind a Session to an externally owned transaction or savepoint and prove
rollback rather than truncating shared state.
