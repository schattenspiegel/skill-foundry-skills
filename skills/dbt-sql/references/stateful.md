# Incremental models and snapshots

An incremental model needs a unique key and explicit semantics for new, late,
changed, and deleted records. Bound the rescan window from observed lateness,
not convenience. Test incremental output against a full refresh on synthetic
changes. Snapshots require a business key, update detection strategy, and hard
delete policy; validate nonoverlapping validity intervals.
