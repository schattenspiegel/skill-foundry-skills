# Portfolio refactor ADR

Status: implemented as a clean-break source migration.

## Decision

Organize the public distribution as a curated core plus pack manifests. Every
source skill declares its kind, quality tier, public/private status, packs, and
target-evidence class in `skill.toml`. Pack manifests are catalogs, not an
installer or runtime dependency mechanism.

## Consolidations

The data-analyst bundle previously duplicated command and support skills. The
following source names are retired:

| Retired | Replacement |
|---|---|
| `data-analyst-core`, `data-context` | `data-analysis-core` |
| `data-exploration` | `data-explore` |
| `diagnostic-analysis` | `data-investigate` |
| `sql-analysis` | `data-query` |
| `data-wrangling` | `data-transform` |
| `analytical-delivery` | `data-deliver` |

No aliases are emitted. The six intent commands remain the user-facing
orchestrators. `local-data`, `spreadsheet-analysis`, `statistical-analysis`, and
`data-validation` remain focused private support skills.

Pydantic runtime data contracts and pydantic-settings source assembly are split
because they have different triggers, dependencies, versioning, and failure
modes.

## Additions

Foundational skills: Excel file engineering, Matplotlib, SQLAlchemy, Python
project tooling, Jupyter, and dbt SQL. Integration skills: DuckDB/Polars,
FastAPI/Pydantic, HTTPX/Tenacity/asyncio, SymPy/NumPy/SciPy, and
scikit-learn/statsmodels.

## Evidence policy

Mock and Codex-proxy results never become target acceptance. Public skills may
be `candidate` or `recommended`; experimental skills remain private. A build
contains only `runtime/`, manifests, pack metadata, license, notices, and the
public README.
