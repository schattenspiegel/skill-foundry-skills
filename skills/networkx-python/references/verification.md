# Verification and API grounding

## Inspect locally

```python
import inspect
import networkx as nx

print(nx.__version__)
print(inspect.signature(nx.shortest_path))
print(nx.get_default_backend() if hasattr(nx, "get_default_backend") else "no API")
```

Use the installed documentation/signature for backends, dispatch keywords,
algorithm availability, and conversion details. The stable authoring reference
was NetworkX 3.6.1:

- <https://networkx.org/documentation/stable/reference/index.html>
- <https://networkx.org/documentation/stable/reference/classes/index.html>
- <https://networkx.org/documentation/stable/reference/algorithms/index.html>

## Behavioral tests

Prefer small graphs whose answer is hand-checkable. Include, as relevant:

- empty and singleton graphs;
- isolated and disconnected nodes;
- both directions of an asymmetric edge;
- duplicate or parallel edges with distinct weights;
- self-loops;
- equal-cost paths and deterministic tie policy;
- missing weight attributes;
- cycle versus DAG;
- a graph with no path and a missing node;
- conversion with isolates and attributes.

Assert graph class, node/edge sets including keys, required attributes, numeric
result tolerance, and output ordering separately. A plausible path on one toy
graph does not prove the weight or direction contract.
