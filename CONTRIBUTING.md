# Development rules

This repo enforces its rules with tooling, not just convention. Everything in
this document is checked by CI on every push — see `.github/workflows/ci.yml`.

## Clean code

- Small, single-responsibility functions. A function does one thing; if you
  need "and" to describe it, split it.
- Descriptive names over comments. Comments explain *why*, never *what* —
  if a comment just restates the code, delete the comment and rename instead.
- Guard clauses over nested conditionals.
- No dead code, no commented-out code, no speculative
  parameters/branches for cases that can't currently happen.
- Cyclomatic complexity is capped at 8 per function, enforced by
  `ruff` (`C90` rule set). If you hit the cap, the function is telling you to
  split it.

## Clean architecture (this world's layering)

Archipelago's `AutoWorld` pattern gives us the seam for free — use it:

| Module | Responsibility | Should contain |
|---|---|---|
| `Items.py` / `Locations.py` | Static data tables | Dicts/dataclasses only. No conditionals. |
| `Regions.py` | Region graph construction | Pure functions: `(multiworld, player) -> None`/regions, built from the tables above. |
| `Rules.py` | Access logic | Pure predicate functions: `(state) -> bool`. No I/O, no randomness, independently callable without running full generation. |
| `Options.py` | Player-facing generation options | Option class definitions + validation only. |
| `__init__.py` | Framework glue | Registers `MGSDeltaWorld`, wires the modules above together. Kept deliberately thin — if you find yourself writing an `if` here, that logic belongs in `Rules.py` or `Regions.py` instead. |

The point of this split: everything that makes a *decision* (`Rules.py`,
non-trivial helpers in `Regions.py`) is a pure function you can unit-test with
plain inputs/outputs, with no `MultiWorld` generation required to exercise it.

## Testing policy: every line of logic is tested

- **100% line coverage is a CI gate**, not a suggestion —
  `pytest --cov --cov-fail-under=100` (see `pyproject.toml`). A PR that drops
  coverage fails CI.
- Coverage alone proves a line *executed*, not that it's *correct*. That's
  what mutation testing is for: **mutmut** rewrites your logic (flips a
  comparison, changes a constant, etc.) and every mutant must be killed by an
  existing test. A surviving mutant means the coverage over that line is
  fake — the test runs it but never actually checks its behavior. Fix
  survivors by strengthening assertions, not by adding a no-op call just to
  bump coverage.
- Practically: `Items.py`/`Locations.py` data tables need no logic tests
  (they're data). Every function in `Rules.py` and every non-trivial helper
  in `Regions.py` needs a test per branch, checked by both coverage and
  mutation testing.
- `__init__.py` framework glue is exercised indirectly via Archipelago's
  `TestBase` generation smoke tests, not unit-tested line by line — because
  it should contain no branches to unit-test in the first place.

### Bootstrapping note

`mutmut` needs at least one real function in the codebase to hook its
self-check into — on a tree of pure stub/docstring files (like this repo
today) it fails with a misleading error. `scripts/run_mutation_tests.py`
detects that state and skips cleanly instead of red-X'ing every commit. The
moment the first real function lands, that exemption disappears and mutation
testing becomes a real, enforced gate — this is intentional, not a
loophole to rely on.

## One intentional lint deviation

`ruff`'s `N999` (module naming) is disabled. Every world in the main
Archipelago repo uses PascalCase filenames (`Items.py`, `Rules.py`, ...) —
we match that convention on purpose so this world doesn't look foreign to
anyone who's touched another AP world.

## Running the checks locally

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"

.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy
.venv/bin/pytest --cov --cov-report=term-missing
.venv/bin/python scripts/run_mutation_tests.py
```

All five must pass before opening a PR — CI runs the exact same commands.
