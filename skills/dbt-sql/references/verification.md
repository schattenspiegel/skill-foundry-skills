# Compile and run verification

Parse/compile to catch graph, macro, and dialect issues before warehouse work.
Inspect compiled SQL for refs, predicates, joins, and adapter dispatch. Run a
bounded selector in the intended target, then tests. Read manifest and run
results but verify actual relation grain, rows, schema, and reconciliations.
Compilation is not execution; successful execution is not validated semantics.
