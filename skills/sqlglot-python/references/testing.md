# Testing SQLGlot transformations

1. Test every supported source/target dialect pair separately.
2. Include malformed SQL, multiple statements, comments, semicolons, quoted and
   case-sensitive identifiers, nested subqueries, CTE shadowing, stars, aliases,
   correlated columns, nulls, and vendor-specific constructs.
3. Assert AST classes and semantic arguments before asserting generated text.
4. Verify the original tree is unchanged when the API promises a copy.
5. Configure unsupported generation to fail and preserve the failing construct
   as a regression.
6. Reparse every generated statement with the target dialect.
7. For equivalence, run representative data through both engines and compare
   schema, values, null behavior, cardinality, and ordering where defined.
8. For an allowlist, try mutating statements, generic commands, nested writes,
   comments, and multi-statement bypasses; still enforce executor permissions.
