# Plotly figure model

A figure is a schema-backed tree serialized to JSON. Its top-level `data` is an
ordered trace list; `layout` contains figure-wide and subplot structures;
`frames` contains animation states. Rendering configuration passed to `show` or
host components is not the same as figure layout.

Plotly Express returns an ordinary graph-objects `Figure`. Discrete color,
symbol, line dash, facets, and animation can multiply traces. Inspect trace
`type`, `name`, `legendgroup`, axis references, and array lengths before applying
updates. Use selectors rather than assuming an index remains stable.

## Data identity

Keep a stable row identifier in `customdata` when clicks/selections must map
back to records. Hover text is presentation, not a reliable ID. Align every
per-point array (text, customdata, marker color/size) with x/y after filtering or
sorting.

Layout axes are named `xaxis`, `xaxis2`, etc., while traces refer to them as
`x`, `x2`, etc. Shapes and annotations can use data or paper coordinates; state
the intended coordinate system so zoom/subplots behave correctly.
