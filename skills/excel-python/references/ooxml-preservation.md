# OOXML preservation

An `.xlsx` or `.xlsm` file is a ZIP package of parts connected by
relationships. Before an openpyxl round-trip, inventory content types, parts,
and relationships. High-risk families include:

- `vbaProject`, ActiveX, controls, embeddings, and OLE objects;
- drawings, shapes, media, charts, chartsheets, slicers, and timelines;
- PivotTables, pivot caches, connections, query tables, external links, and
  Power Query/custom-data artifacts;
- custom XML, threaded comments/persons, custom properties, signatures, and
  uncommon or unknown relationship types.

Classify each finding as supported for the intended mutation, pass-through
verified, unsupported, or unknown. `unsupported/unknown + must preserve` means
no blind openpyxl save. Preserve the original and require an installed-Excel or
other proven path with separate authority.

For allowed changes, snapshot package inventory and hashes before writing, save
to a new path, reopen, and run the semantic diff. Exact ZIP bytes, timestamps,
relationship IDs, XML ordering, and serialization can change without semantic
change, so raw-byte equality is not the comparison contract. Require exact hash
preservation only for opaque parts such as `vbaProject.bin` when appropriate.
