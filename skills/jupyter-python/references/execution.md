# Execution and verification

Use nbclient or `jupyter execute` with an explicit kernel, working directory,
timeout, and default stop-on-error behavior. Save a separate executed artifact.
Assert no error outputs, expected files/tables/figures, bounded output size, and
the relevant results. Run twice from clean state when nondeterminism matters.
