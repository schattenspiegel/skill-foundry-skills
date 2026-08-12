# Object and data model

## Identity and topology

- A node is a hashable Python value. Equality and hashing define identity; an
  attribute such as `id` does not unless it is itself the node key.
- Simple graphs store at most one edge per endpoint pair. Adding the pair again
  updates edge data. Multigraphs assign an edge key and preserve parallel edges.
- Undirected edges have no source/target meaning. Directed predecessors and
  successors are different relationships.
- Self-loops are allowed by all four standard graph classes; reject them at
  ingestion if the domain forbids them.

## Data mappings and views

`G.graph`, `G.nodes[node]`, and `G.edges[u, v]` are mutable attribute mappings.
Multigraph edge lookup includes the key: `G.edges[u, v, key]`. Prefer stable,
documented attribute names and validate required data at the boundary.

`G.nodes`, `G.edges`, adjacency mappings, subgraph views, reverse views, and
filtered views reflect graph mutations. Use a view for a live projection; use
`.copy()` for independently mutable topology. Attribute values may still be
nested mutable objects, so state whether shallow copying is sufficient.

## Return-shape anchors

- `G.neighbors(node)` and many algorithms return iterators.
- `G.degree` is a view; `G.degree[node]` is one number.
- `nx.connected_components(G)` yields sets and applies to undirected graphs.
- Strong and weak components are distinct directed-graph concepts.
- Single-source path APIs often return mappings; source-target APIs return one
  path or length. Inspect the exact family rather than guessing by name.
- A multigraph edge iteration needs `keys=True` to retain edge identity and
  `data=True` to retain attributes.

## Conversion contract

Before converting, list what must survive: node identity, directedness,
parallel-edge keys, graph/node/edge attributes, isolated nodes, numeric dtype,
and ordering. Adjacency matrices cannot represent arbitrary Python node labels
without a separate node order, and many tabular formats do not preserve edge
keys automatically. Assert a round trip only for properties the format can
represent.
