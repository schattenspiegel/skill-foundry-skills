# Plotly composition, facets, and events

Use Express facets for homogeneous small multiples from one dataframe contract.
Use `make_subplots` for heterogeneous trace types, secondary axes, domain/3D/map
specs, or exact grid spans. After composition, verify every trace's x/y axis or
subplot reference.

Shared matched scales permit magnitude comparison; independent ranges reveal
within-panel variation but can mislead cross-panel comparison. Encode and test
the choice. Fix facet/legend order with category orders rather than sorting only
display labels after figure creation.

## Event boundary

Trace `.on_click`/hover/selection callbacks require a displayed `FigureWidget`
in a compatible ipywidgets environment. `fig.show()`, static HTML, image export,
and an ordinary `Figure` do not execute Python callbacks. Dash, Streamlit, and
other hosts expose their own event/selection channels; keep state in that host.

For event-driven code, store stable IDs in customdata, validate selected point
indices, handle empty selections, and batch figure mutations where the widget
API supports it. Never place secrets in customdata: the serialized figure can
reach the browser.
