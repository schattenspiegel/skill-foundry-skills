# Verification and grounding

Primary sources inspected 2026-08-12:

- <https://www.rustworkx.org/api/index.html>
- <https://www.rustworkx.org/api/graph_classes.html>
- <https://www.rustworkx.org/networkx.html>

The current API index labels release 0.18.1. Some individual generated pages
can retain older release labels, so verify the installed version and use
`inspect.signature` where available. Extension functions may expose
positional-only parameters; the Dijkstra length function explicitly does.

Behavioral tests should build a graph, remove an interior node, add another,
and prove the mapping still identifies domain nodes. Add parallel edges with
different payload costs and prove exact edge/result selection. Cover reverse
direction, unreachable nodes, missing/nonfinite costs, conversion isolates, and
callback exceptions. Compare performance only after correctness tests and with
representative topology, payloads, callback cost, and conversion overhead.
