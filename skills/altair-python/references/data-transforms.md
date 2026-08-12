# Altair data and transforms

## Choose the execution side

Use Python preprocessing for reusable/domain data contracts, joins requiring
validation, sensitive filtering that must occur before browser delivery, and
work requiring a library unavailable in Vega-Lite. Use declarative transforms
for chart-local calculate/filter/bin/aggregate/window/fold/lookup behavior and
parameter-driven changes.

Filters in the visualization do not enforce data access control: data embedded
in or reachable by the spec may still reach the browser. Remove sensitive rows
and fields before chart construction.

## Transform order

Transforms form an ordered pipeline. Calculate before using the derived field;
filter before aggregate when the aggregate should see only retained rows;
aggregate before window/rank when ranking summaries; and retain every required
group field. Test the transform list order in `chart.to_dict()`.

## Data transport

Inline values make a portable spec but grow notebooks/HTML and hit safeguards.
URL data requires availability/CORS and can make a previously portable artifact
environment-dependent. Named/consolidated datasets avoid duplicate inline data
in compound specs. File-backed data transformers may write adjacent temporary
files whose portability differs from inline specs.

When a maximum-row error occurs, choose one of: upstream aggregation/filtering,
intentional external data, or a measured supported transformer. Sampling is
valid only when the question tolerates sampling and the sample policy is part
of the result.
