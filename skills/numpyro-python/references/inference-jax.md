# NumPyro inference and JAX execution

## MCMC

Use NUTS/HMC for continuous differentiable latent states. Run multiple chains
when diagnostics require between-chain comparison, collect relevant extra
fields, and inspect divergences, acceptance behavior, tree depth, R-hat, ESS,
MCSE, and traces after conversion to a labeled diagnostic form. Reparameterize
hierarchies and standardize scales before raising acceptance targets alone.

## SVI

Choose a guide that can represent required posterior dependence and support.
Initialize from multiple keys, monitor loss without interpreting it as model
evidence, validate predictive draws, and compare against MCMC on a smaller
synthetic/real subset where possible. Minibatching requires a correctly sized
plate so log-density scaling is valid.

## JAX

Set x64/precision policy before creating arrays and compiling. JIT cache keys
depend on shapes, dtypes, and static arguments; use stable padded/bucketed shapes
when compilation churn matters. Split or fold PRNG keys at explicit ownership
boundaries. Inspect devices before selecting parallel chain execution. A seeded
run may still vary across hardware/compiler versions; record environment for
strict reproducibility.
