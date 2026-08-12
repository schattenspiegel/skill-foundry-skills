# Progress and Live lifecycle

## Choose the controller

Use `console.status` for one indeterminate foreground operation. Use `track` for
one known iterable with standard presentation. Use `Progress` for multiple
tasks, manual advancement, custom columns, or shared console output. Use `Live`
for a changing table, tree, panel group, or dashboard.

## Invariants

- Enter and exit through a context manager.
- Advance only after the represented work unit commits.
- A task's `total` and `completed` use the same unit.
- Set `total=None` for genuinely indeterminate work; do not invent percentages.
- Retain task IDs instead of finding tasks by display text.
- Avoid nested live controllers on the same console.
- Print messages through `progress.console` or the shared live console.
- Throttle updates; rendering must not dominate the workload.

For redirected output and CI, accept Rich's noninteractive behavior. Do not
force cursor-control sequences into files. If an application needs durable
progress logs, emit separate structured/log records at coarse state changes;
the animated display is not the audit trail.

## Failure handling

Update task description/status only if doing so cannot mask the original
exception. Let the context manager restore the terminal, then propagate or map
the failure at the CLI boundary. A transient display must not swallow errors or
turn a failed job into a visually completed bar.
