# Skill Foundry Skills

This is the sanitized runtime distribution of Agent Skills built by Skill
Foundry. It contains only compiled skill directories, external manifests, pack
manifests, the license, and notices. Authoring research, evaluation fixtures,
private orchestration skills, and foundry tooling are excluded.

## Evidence labels

- **recommended**: the strongest deterministic evaluation coverage in this
  portfolio; target-host acceptance is reported separately.
- **candidate**: structurally valid with bounded evaluation coverage, but still
  requires more semantic or target-host evidence.
- **target_evidence: not_run**: no GitHub Copilot acceptance claim.
- **target_evidence: diagnostic_proxy**: proxy evidence only; not acceptance.
- **target_evidence: copilot_accepted**: repeated conforming target-host evidence
  has been recorded by the private foundry.

`catalog.json` is the canonical machine-readable inventory. `packs/*.json`
provides curated groupings without introducing an installer.

## Install one skill

Copy `skills/NAME/` to either:

- `~/.copilot/skills/NAME/` for personal GitHub Copilot use; or
- `.github/skills/NAME/` in a repository.

Verify current locations and customization behavior in the installed VS Code
host before relying on them. Third-party libraries are not included.
