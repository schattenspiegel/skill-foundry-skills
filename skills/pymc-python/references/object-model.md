# PyMC model and shape contract

## Graph roles

A `Model` owns named inputs and probability nodes. `Data` conditions the graph;
unobserved random variables are sampled; an observed random variable contributes
the likelihood; a `Deterministic` names a derived expression; a `Potential` is
registered under a name and adds log density without becoming a random variable
or gaining a generative sampling rule.

## Shape checklist

For each non-scalar variable record:

- support dimensions inherent to one draw from its distribution;
- batch dimensions indexing independent parameter instances;
- named model dimensions and coordinate values;
- the concrete observed/data array shape.

Test that coordinate lengths match their axes and index arrays fall within the
referenced coordinate. Give group effects the group dimension, observation
effects the observation dimension, and coefficient arrays the feature
dimension. Do not repair a mismatch by adding a broadcast axis until the
generative meaning is known.

## Data updates

`Data` is the prediction boundary. When observation count or labels change,
replace values and the corresponding coordinates together using the installed
API. Category encodings and feature order must reuse training semantics.
Changing a data container recomputes dependent deterministics during prediction;
inspect current posterior-predictive volatility rules before relying on finer
freeze/resample controls.
