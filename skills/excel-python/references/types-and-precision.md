# Types and precision

## Classify before writing

| Semantic type | Workbook policy |
|---|---|
| Identifier/code | Store as text when arithmetic is meaningless or more than 15 significant digits is possible; preserve leading zeroes. |
| Measure | Store as numeric only after defining unit, scale, acceptable binary floating behavior, and rounding. |
| Exact decimal | Compute/round under the declared Decimal policy before conversion; Excel numeric cells still use floating-point precision. |
| Missing | Choose blank cell, formula error, sentinel text, or zero explicitly. `None`, blank, and `""` are not interchangeable. |
| Non-finite float | Reject or map explicitly; never silently turn `NaN`/infinity into ordinary text or zero. |
| Boolean | Store as boolean unless the contract requires a label. |
| Date/datetime | Preserve workbook epoch; define timezone conversion before removing timezone information. |

Excel numeric precision is limited to 15 significant digits. A number format
changes only display: `0.00` does not round the stored value, and displayed
values need not be the inputs used by formulas. Perform contract-required
rounding in the value or formula and test boundary cases.

Percent values are normally stored as ratios (`0.12` displayed as `12%`). Basis
points, currencies, scaled thousands/millions, and FX rates require explicit
stored unit and displayed unit. Put units in headers, names, or nearby labels;
do not rely on color or formatting alone.

Excel supports 1900 and 1904 date systems, separated by 1,462 days. Inspect the
source epoch, preserve it during mutation, and test known dates after reopening.
Do not write timezone-aware Python datetimes directly; convert under a declared
zone/DST policy and record whether the workbook stores local wall time or UTC.
