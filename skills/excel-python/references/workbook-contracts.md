# Workbook contracts

A workbook contract is the semantic interface that makes addresses meaningful.
Recover or define:

- workbook purpose, supported Excel consumers, and delivery format;
- sheet roles, order, visibility, and whether hidden logic is permitted;
- Excel Table names/ranges and defined names;
- input and output row grain, keys, ordering, and units;
- identifier, measure, blank, error, date/time, and rounding policies;
- formula-owned columns and exceptional constants;
- user-editable, protected, presentation-only, and machine-readable areas;
- chart sources, validation lists, print/PDF requirements, and provenance;
- features and package parts that must be preserved;
- calculation owner and the evidence required after calculation.

Prefer stable semantic interfaces in this order:

`cell address < rectangular range < defined name < Excel Table < workbook contract`

The hierarchy is not absolute: a regulatory template may contractually require
`F17`. Record that as a named interface in the contract rather than scattering
the address through code.

Before mutation, assert that discovered Tables, names, headers, keys, formulas,
and units match the contract. Stop on ambiguity rather than guessing from sheet
names or visual proximity.
