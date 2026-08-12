# Indices, payloads, and ownership

`PyGraph` and `PyDiGraph` store topology in native graph structures while node
and edge payloads remain Python objects. APIs may call a payload a “weight” even
when it is not numeric. Algorithmic weights are normally derived with a
callback.

Adding a node returns its integer index. Adding an edge returns an edge index.
Indices remain valid while the item exists, but removal can create gaps and an
index can be reused. Maintain explicit maps:

```python
index_by_id: dict[str, int]
id_by_index: dict[int, str]
```

Update both under graph mutation, or rebuild them from payloads after a
transformation whose index mapping is returned. Subgraph/conversion APIs may
return a new graph and mapping; preserve that mapping rather than inferring it.

By default graphs support parallel edges. With `multigraph=False`, adding an
edge between existing endpoints updates the existing payload. Decide this at
construction because the wrong policy loses relationship identity.
