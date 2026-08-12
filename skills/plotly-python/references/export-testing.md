# Plotly export and semantic testing

Return figures from builders. At the edge choose:

- dict/JSON for schema inspection or a figure consumer;
- HTML for interactive standalone/embed output, with explicit CDN/bundled JS
  portability policy;
- image/vector export only after verifying the installed image engine;
- FigureWidget only in the supported notebook widget host.

Test `fig.to_dict()` semantically: trace types/count/order/names, aligned arrays,
customdata IDs, axis references, layout titles/units, category order, facet
annotations, legend/color axis, frames, and sensitive-field absence. Avoid whole
figure snapshots because default templates and generated IDs drift.

Render smoke tests must cover empty and null data, long labels, narrow width,
large point counts, tooltip correctness, and the actual host. A valid JSON tree
does not prove browser JavaScript, widget comms, fonts, maps, or image export.
