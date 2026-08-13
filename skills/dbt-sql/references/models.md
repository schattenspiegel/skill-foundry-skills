# Graph and model design

Sources describe external relations; refs describe managed graph dependencies.
Each model declares a grain and testable contract. Use staging models for source
normalization, intermediate models for reusable transformations, and marts for
consumer-facing entities when those layers match project conventions. Avoid
models that exist only to rename a CTE without creating a reusable boundary.
