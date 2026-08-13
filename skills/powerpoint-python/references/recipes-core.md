# Evaluated recipes

## Recipe `powerpoint.template-contract`
**Use when:** generating against a supplied professional template.
**Inspect first:** dimensions, masters, layout names, placeholder indices/types/geometry.
**Invariants:** unique semantic layout match; no positional guess; source template unchanged.
```python
from pathlib import Path
from pptx import Presentation

def layouts_by_name(template: Path) -> dict[str, list[int]]:
    prs = Presentation(template)
    result: dict[str, list[int]] = {}
    for index, layout in enumerate(prs.slide_layouts):
        result.setdefault(layout.name, []).append(index)
    return result
```
**Do not use when:** exact layout identity remains ambiguous.
**Verify:** run `inspect_template.py` and bind placeholder `idx` values.

## Recipe `powerpoint.atomic-generation`
**Use when:** publishing a newly generated `.pptx`.
**Inspect first:** destination, overwrite policy, template, contract.
**Invariants:** template-first; temporary sibling; reopen before publication.
```python
from pathlib import Path
from pptx import Presentation

def build(template: Path, destination: Path, render) -> None:
    prs = Presentation(template)
    render(prs)
    temporary = destination.with_name(f".{destination.stem}.tmp{destination.suffix}")
    prs.save(temporary)
    Presentation(temporary)
    temporary.replace(destination)
```
**Do not use when:** editing a preservation-sensitive source without preflight/diff.
**Verify:** validate the temporary artifact and run relevant project checks.

## Recipe `powerpoint.preservation-preflight`
**Use when:** changing an existing valuable `.pptx` or `.pptm`.
**Inspect first:** package parts, relationships, unknown content, VBA/timing/diagrams/notes.
**Invariants:** source unchanged; active content never executed; unsupported required parts escalate.
```python
import hashlib
import zipfile

def part_hash(path, name):
    with zipfile.ZipFile(path) as archive:
        try:
            return hashlib.sha256(archive.read(name)).hexdigest()
        except KeyError:
            return None
```
**Do not use when:** a native runtime operation is the actual requirement.
**Verify:** semantic diff and required opaque-part hashes after save.
