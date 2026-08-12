# Evaluated solution recipes

## Recipe `subprocess.safe-argv-json`
**Use when:** execute untrusted-looking values as argv data.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import json
import subprocess


def run_json_tool(executable: str, payload: str, timeout: float = 5.0) -> object:
    completed = subprocess.run(
        [executable, "--payload", payload],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
        timeout=timeout,
        shell=False,
    )
    return json.loads(completed.stdout)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`safe-argv-command`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `subprocess.verify-argv-boundary`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import json
import os
from pathlib import Path
from solution import run_json_tool


def test_payload_is_one_argument(tmp_path: Path) -> None:
    tool = tmp_path / "tool"
    tool.write_text("#!/usr/bin/env python3\nimport json,sys\nprint(json.dumps(sys.argv[2]))\n")
    tool.chmod(0o755)
    payload = "x; echo injected && $(false)"
    assert run_json_tool(str(tool), payload) == payload
```
**Do not use when:** The requested abstraction or lifecycle differs from
`safe-argv-command`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `subprocess.stdin-text-protocol`
**Use when:** send a secret-like payload over stdin with bounded completion.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import subprocess


def call_filter(executable: str, payload: str, timeout: float) -> str:
    if timeout <= 0:
        raise ValueError("timeout must be positive")
    completed = subprocess.run(
        [executable],
        input=payload,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
        timeout=timeout,
    )
    return completed.stdout.removesuffix("\n")
```
**Do not use when:** The requested abstraction or lifecycle differs from
`bounded-stdin-protocol`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `subprocess.verify-stdin-secret`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import sys
from pathlib import Path
import pytest
from solution import call_filter


def test_stdin_round_trip(tmp_path: Path) -> None:
    tool = tmp_path / "tool.py"
    tool.write_text("import sys\nprint(sys.stdin.read()[::-1])\n")
    wrapper = tmp_path / "wrapper"
    wrapper.write_text(f"#!/bin/sh\nexec {sys.executable} {tool}\n")
    wrapper.chmod(0o755)
    assert call_filter(str(wrapper), "secret", 2) == "terces"
    with pytest.raises(ValueError):
        call_filter(str(wrapper), "x", 0)
```
**Do not use when:** The requested abstraction or lifecycle differs from
`bounded-stdin-protocol`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `subprocess.communicate-dual-pipe`
**Use when:** drain stdout and stderr without pipe deadlock.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import subprocess
from collections.abc import Sequence


def capture_both(argv: Sequence[str], timeout: float = 5.0) -> tuple[bytes, bytes]:
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        process.communicate()
        raise
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, argv, stdout, stderr)
    return stdout, stderr
```
**Do not use when:** The requested abstraction or lifecycle differs from
`large-dual-pipe`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.

## Recipe `subprocess.verify-large-pipes`
**Use when:** verify the implementation contract.
**Inspect first:** Confirm Python and installed package versions, input shapes,
ownership, and the caller's error contract before adapting this anchor.
**Invariants:** Preserve the scenario's ownership, ordering, failure, and
completion guarantees; do not weaken an assertion merely to make it pass.
```python
import sys
from solution import capture_both


def test_large_streams_do_not_deadlock() -> None:
    code = "import sys;sys.stdout.buffer.write(b'x'*200000);sys.stderr.buffer.write(b'y'*200000)"
    stdout, stderr = capture_both([sys.executable, "-c", code], 5)
    assert len(stdout) == len(stderr) == 200000
    assert stdout[:1] == b"x" and stderr[:1] == b"y"
```
**Do not use when:** The requested abstraction or lifecycle differs from
`large-dual-pipe`; select the nearest decision branch instead.
**Verify:** Run `python -m pytest -q` in the declared project environment and
exercise both the success path and the named edge or failure path.
