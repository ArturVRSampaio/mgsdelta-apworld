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
self-check into — on a tree of pure stub/docstring files it fails with a
misleading error. `scripts/run_mutation_tests.py` detected that state and
skipped cleanly instead of red-X'ing every commit. That exemption no longer
applies: the frog-skeleton milestone landed real functions, so mutation
testing is now a real, enforced gate.

### Archipelago core dependency

This world needs real Archipelago core (`worlds.AutoWorld`, `BaseClasses`,
`test.bases`, ...) to mean anything — it's vendored as a pinned git
submodule at `Archipelago/` (currently tag `0.6.7`) rather than a pip
dependency, since it isn't published as an installable package.
`conftest.py` puts it on `sys.path` and forces `SKIP_REQUIREMENTS_UPDATE=1`
so importing it doesn't trigger its interactive dependency-update prompt.
Ruff/mypy are configured to not lint or type-check the submodule itself
(see `pyproject.toml`) — it's vendored code we don't own.

`mutmut` imports Python's `resource` module, which doesn't exist on
Windows — the mutation gate can only actually run on Linux/macOS (CI uses
`ubuntu-latest`). On Windows, `scripts/run_mutation_tests.py` will report
false success without ever running a mutant; don't trust a local "All
mutants killed" on that platform.

Mutating the whole `mgsdelta/` tree on every run gets slow as real logic
accumulates. `scripts/run_mutation_tests.py` scopes each run to just the
`.py` files changed since the best available base ref (PR base ref,
`origin/main`, or the previous commit) by temporarily rewriting
`pyproject.toml`'s `paths_to_mutate` and restoring it afterward — mutmut
itself has no CLI/env override for this, only a pyproject.toml key. If no
base ref resolves at all (e.g. a single-commit shallow clone), it falls
back to mutating everything.

## One intentional lint deviation

`ruff`'s `N999` (module naming) is disabled. Every world in the main
Archipelago repo uses PascalCase filenames (`Items.py`, `Rules.py`, ...) —
we match that convention on purpose so this world doesn't look foreign to
anyone who's touched another AP world.

## Running the checks locally

```bash
git submodule update --init  # first time only, fetches Archipelago/ core

python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pip install -r Archipelago/requirements.txt  # needed for pytest/mutmut, not lint

.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/mypy
.venv/bin/pytest --cov --cov-report=term-missing
.venv/bin/python scripts/run_mutation_tests.py
```

All five must pass before opening a PR — CI runs the exact same commands.
The mutation step can only run on Linux/macOS; see the Windows caveat above.
