# Core and ORM decisions

Core expresses schemas and SQL statements without identity-map semantics. ORM
adds mapped identity, relationships, cascades, and unit-of-work flushes. Use
`select()` in both. Prefer scalar accessors only when result shape is known.
Materialize cursor-backed results before leaving their resource scope. Make
loading strategy match cardinality; joined collection loads can multiply rows.
