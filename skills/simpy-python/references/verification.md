# Verification and grounding

Primary authoring sources:

- <https://simpy.readthedocs.io/en/stable/>
- <https://simpy.readthedocs.io/en/stable/topical_guides/events.html>
- <https://simpy.readthedocs.io/en/stable/topical_guides/resources.html>
- <https://simpy.readthedocs.io/en/stable/topical_guides/environments.html>

Inspect `simpy.__version__` and signatures in the project environment. Test a
hand-calculated schedule with exact transition times before a stochastic model.
Then cover simultaneous events, capacity contention, resource interruption,
zero duration, a horizon boundary, censored entities, and repeatability under a
fixed seed. A mock evaluation proves the grader wiring only; it does not validate
SimPy execution when the package is absent.
