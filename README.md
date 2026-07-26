# mgsdelta-apworld

[![CI](https://github.com/arturvrsampaio/mgsdelta-apworld/actions/workflows/ci.yml/badge.svg)](https://github.com/arturvrsampaio/mgsdelta-apworld/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/arturvrsampaio/mgsdelta-apworld/graph/badge.svg)](https://codecov.io/gh/arturvrsampaio/mgsdelta-apworld)

Archipelago "world" implementation for **Metal Gear Solid Δ: Snake Eater**.

This is the piece that plugs into the Archipelago **generator/server**. It defines
what items and locations exist, how they're connected (regions), what logic gates
access to what, and what options a player can configure. It has **no idea a game is
running** — it never touches MGS Δ directly. That's the job of the companion
[`mgsdelta-connector`](../mgsdelta-connector) repo.

If you're new to Archipelago world development, read
[Archipelago's world API docs](https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/AutoWorld.py)
and an existing simple world (e.g. `worlds/clique` in the main repo) before diving in
here — this README assumes that context.

## Install

```bash
git clone --recurse-submodules https://github.com/ArturVRSampaio/mgsdelta-apworld.git
cd mgsdelta-apworld
# if you cloned without --recurse-submodules:
#   git submodule update --init

python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pip install -r Archipelago/requirements.txt  # real Archipelago core, needed to run tests
```

Then `.venv/bin/pytest --cov` should pass. See [`CONTRIBUTING.md`](./CONTRIBUTING.md)
for the full check suite (lint, types, mutation testing) and a Windows caveat
on the mutation step.

## Layout

```
mgsdelta/
  __init__.py     # World class registration (MGSDeltaWorld(World))
  Items.py        # Item name/ID table + item groups
  Locations.py     # Location name/ID table + location groups
  Regions.py       # Region graph + entrances (mirrors the game's map)
  Rules.py         # access_rule / item_rule logic for regions & locations
  Options.py       # per-player generation options
  data/            # static data tables (json/yaml) once we have real IDs
  test/            # Archipelago TestBase test cases
```

## Design plan

### Item pool (draft, subject to change once we scope the connector's reach)
- **Progression**: key items (ID cards, memory ampoule/keys), boss-required gear
  (thermal goggles, mine detector), story-gating camo if any.
- **Useful, non-required**: weapons, camo patterns, face paints, weapon upgrades.
- **Filler**: rations, medicine, ammo, cigarettes/binoculars-type non-required items.
- **Traps** (optional, opt-in via Options): hunger-drain trap, radio-static trap,
  stamina-drain trap — all things the base game already has mechanics for, so no
  new game behavior needs to be invented, only triggered.

### Location pool (draft)
- All 64 Kerotan **frogs** (great low-stakes filler-heavy check pool, easy to
  reason about logic for since they're mostly just "reachable" checks) — and/or
  the 64 Gako **ducks**, a same-shape collectible on the same in-game
  subsystem. **The connector confirmed reading the duck counter live before
  the frog one** (see `mgsdelta-connector`'s README/NOTES), so ducks are the
  current frontrunner to be the real first-implemented location set once this
  world grows past the skeleton milestone — frogs remain the flavor-preferred
  choice if/when their equivalent read is confirmed too.
- Weapon/item pickup spots.
- Cobra Unit boss defeats (The Pain, The Fear, The End, The Fury, The Sorrow,
  The Boss) as location checks with their vanilla reward as the local placement,
  or fully randomized — TBD via an Option.
- GA doc animal-capture milestones, if the connector can detect them reliably.

### Regions & logic
Region graph will mirror the game's actual area connectivity (Dolinovodno →
Ravine → Bolshaya Past forest → Ponizovje swamp → Groznyj Grad → Volgin's chapters),
built from a real playthrough map, not guesswork. Logic rules will encode things
like "needs thermal goggles to reach The End's fight" or "needs the specific key
item to open a specific storage door," matched 1:1 against what the connector can
actually verify ownership of at runtime.

### Options (draft)
- Goal (defeat The Boss vs. some other endpoint if one makes sense).
- Frog checks on/off (some players may not want 64 extra checks).
- Boss reward shuffle on/off.
- Camo/item pool scope (full shuffle vs. key-items-only for a lighter first release).
- Trap frequency, if traps are included at all.

## Build plan / milestones

1. **Skeleton world**: register `MGSDeltaWorld`, pass Archipelago's generic
   `worlds/test` smoke tests with a *minimal* item/location set (frogs only —
   they need no logic beyond reachability). No real game needed for this step.
2. **Region graph v0**: hand-build the full map graph from a documented
   playthrough (video/wiki cross-referenced), independent of the connector.
3. **Logic v0**: encode access rules for the minimal item set against the v0
   region graph; validate with Archipelago's built-in logic sanity checks
   (`--race`/spoiler generation, fill-time errors).
4. **Grow item/location tables** in lockstep with what the connector repo has
   confirmed it can detect/grant (see that repo's milestones) — no location goes
   in here until the connector can actually check it, no item goes in here until
   the connector can actually grant it.
5. **Options polish + docs** (`docs/en_Metal Gear Solid Delta.md`,
   `docs/setup_en.md`) to Archipelago's world-submission standard.
6. **Package as `.apworld`** and dogfood a real multiworld generation + solo game.

## Status

As of 2026-07-26: build plan #1 (skeleton world) is done — `MGSDeltaWorld`
registers, all 64 Kerotan frogs exist as locations in a single "Menu"
region with no traversal logic yet, and the world generates/fills/completes
against real Archipelago core (vendored as a pinned submodule at
`Archipelago/`, tag `0.6.7` — see `CONTRIBUTING.md`). Item pool is a single
placeholder filler item; there's no real region graph, logic, or goal yet.
Next concrete step is #2 (region graph v0). The connector's recon phase is
now done too (UE4SS confirmed working — see that repo's README/NOTES), so
both repos are free to move on their next milestones independently.

## Development

Clean code/architecture rules, the 100%-logic-tested policy, and how to run
the full check suite locally are in [`CONTRIBUTING.md`](./CONTRIBUTING.md).

CI and Codecov are already fully configured and working (verified
2026-07-26) — no setup needed.

## Upstream submission checklist (once the world is functional)

Not relevant yet — revisit once the build plan's milestones above are done
(a real region graph, real logic, a playable goal). Two distribution paths,
pick one when the time comes:

- **Standalone `.apworld`**: package with Archipelago's "Build APWorlds"
  launcher tool. Needs an `archipelago.json` manifest (`game` is required;
  `world_version`/`authors` recommended). No review or notification needed —
  build it and share it.
- **Merged into Archipelago core** (`ArchipelagoMW/Archipelago`'s `worlds/`
  folder, ships to every AP install): fork that repo, move this package to
  `worlds/mgsdelta/`, open a normal PR. Reaching out on Discord's
  `#ap-world-dev` channel first is recommended, not mandatory. After merge,
  this becomes an ongoing **world maintainer** role: stay reachable on
  Discord for issues/updates on this world, review (or arrange review of)
  PRs touching it, fix breakage when core changes affect it, periodically
  test against `main` (especially during RC phases), and give notice before
  extended absences.

Either path needs, before it's ready:
- A `WebWorld` instance wired into `__init__.py`.
- At least one setup guide and one game info page
  (`docs/setup_en.md` / `docs/en_Metal Gear Solid Delta.md`, per the build
  plan above).

## License

[MIT](./LICENSE) — matches Archipelago core's own license, since this world
is meant to eventually plug into it.
