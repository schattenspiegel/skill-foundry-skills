# Operation and algorithm map

## Construction and mutation

Use `add_nodes_from` for isolated nodes and attributes; an edge list alone loses
isolates. For simple graphs, decide whether duplicate edges are an error or an
attribute update before calling `add_edges_from`. For multigraphs, retain the
returned/provided edge key wherever later updates or provenance need it.

## Paths and traversal

- Use BFS/unweighted shortest paths when every edge has equal cost.
- Use Dijkstra for nonnegative additive weights.
- Use Bellman-Ford-family algorithms only when negative weights are meaningful;
  detect negative cycles.
- For A*, the heuristic must not overestimate if optimality is required.
- No path is different from a missing node. Handle the two exceptions
  separately when callers need different messages.

Traversal order can depend on adjacency insertion order. If several paths or
topological orders are equally valid but output must be stable, encode a
neighbor or lexicographical ordering rule.

## Directed and component analysis

Validate DAG status before topological, transitive-reduction, or critical-path
logic. For directed connectivity, choose strong (mutual reachability) or weak
(direction ignored) deliberately. For an undirected graph, define whether an
algorithm applies per component or requires a connected graph.

## Centrality, community, and matrices

Centrality measures answer different questions and can have convergence,
normalization, directedness, or disconnected-graph conditions. Name the domain
meaning before choosing one. Community algorithms may be stochastic or return
sets in unspecified order; seed them where supported and canonicalize output
only at the boundary.

Matrix conversion requires an explicit node list whenever row/column identity
must be recoverable. Treat zeros versus absent edges, parallel-edge aggregation,
and dtype as part of the conversion contract.
