# Skill Foundry Skills

Compiled Agent Skills for GitHub Copilot Agent Mode and other Agent
Skills-compatible hosts.

This repository is distribution-only. It contains runtime instructions,
one-hop references, and optional runtime helpers. Authoring research,
evaluation cases, hidden graders, baselines, and Skill Foundry source code are
maintained separately.

## Install a skill

For a repository-scoped GitHub Copilot skill, copy one directory into the
target repository:

```text
skills/<name>/  ->  <target-repository>/.github/skills/<name>/
```

For a personal GitHub Copilot skill, copy it into:

```text
~/.copilot/skills/<name>/
```

The copied directory itself is the skill root and contains `SKILL.md`.

## Included skills

- Data and validation: Polars, PyArrow, DuckDB, Pydantic and Pydantic
  Settings, Pandera for Polars, SQLGlot, and NumPy.
- Python application libraries: Structlog, Typer, Rich, Tenacity, orjson, and
  xxhash.
- Visualization and apps: Altair, Great Tables, Plotly, and Streamlit.
- Graphs and simulation: NetworkX, rustworkx, and SimPy.
- Mathematics and optimization: CVXPY, SymPy, and mpmath.
- Bayesian modeling and analysis: PyMC, NumPyro, ArviZ, and Bambi.

Each file in `manifests/` records the source skill version and SHA-256 hashes
for the corresponding compiled artifact.

## Evidence boundary

These are compiled runtime artifacts, not a claim that every skill has passed
every target host. Structural validation and distribution builds pass for all
skills. Package-level behavioral coverage varies by library. GitHub Copilot
model acceptance and the final Visual Studio Code smoke test must be performed
in the consumer's environment.

## License

Original material in this repository is licensed under MIT. The referenced
libraries remain independent works under their own licenses; no library package
or vendor source code is bundled here. See [LICENSE](LICENSE) and
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Project and product names are used only to identify compatibility. This project
is not affiliated with or endorsed by the referenced maintainers, GitHub,
Microsoft, or OpenAI.
