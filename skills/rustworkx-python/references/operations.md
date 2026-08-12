# Operations and algorithms

## Construction and lookup

Prefer bulk additions when data is ready, but retain returned indices. Use
`node_indices()`/`edge_indices()` for actual handles, `nodes()`/`edges()` for
payloads, and weighted/index maps when both are required. Do not `range(len(...))`
after deletion.

## Algorithms

Choose directed or undirected function families. Before a shortest-path call,
define source/target index, numeric edge-cost callback, negative-cost policy,
unreachable behavior, and whether the result is a path, mapping, length, or
custom return type. For DAG work, enforce acyclicity at mutation or validate it
before the algorithm.

In the current documented API, the directed Dijkstra length callback is
positional-only:

```python
lengths = rx.digraph_dijkstra_shortest_path_lengths(
    graph,
    source_index,
    lambda payload: float(payload["cost"]),
    goal=target_index,
)
```

Do not write `edge_cost_fn=...` for this function. It raises `TypeError` before
the traversal starts. Other algorithms can expose different callback names and
positions, so inspect their signatures separately.

Traversal APIs may use visitor objects and control flow. Keep visitor state
local, ensure callbacks are deterministic, and do not mutate topology during an
algorithm unless the installed contract allows it.

## Conversion

For NetworkX conversion, check directedness, multigraph flag, isolates, graph
attributes, node payload choice, edge payload/key representation, and returned
node mapping. For matrix conversion, retain the node order that gives matrix
rows and columns their identity.
