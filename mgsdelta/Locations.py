"""
Location name/ID table + location groups for MGS Delta.

Skeleton milestone (build plan #1): the 64 Kerotan frogs — minimal logic,
good first milestone (see README "Location pool"). Build plan #4 growth:
the 64 Gako ducks, added once mgsdelta-connector confirmed (see that repo's
research/NOTES.md milestone 4) it can both detect a duck being collected
and remotely trigger one via the "Unlock Duck" item. Weapon/item pickups,
Cobra Unit boss defeats, and GA doc milestones land once mgsdelta-connector
confirms it can detect them too.

A location only belongs in this table once mgsdelta-connector has confirmed
it can actually detect the corresponding in-game event. Frog and duck IDs
share this module's 1000-wide range (see Items.py), assigned in the order
each set was added so neither renumbers the other.
"""

from __future__ import annotations

from BaseClasses import Location

BASE_ID = 3_901_000

FROG_COUNT = 64

FROG_LOCATION_NAMES = [f"Kerotan Frog {i}" for i in range(1, FROG_COUNT + 1)]

DUCK_COUNT = 64

DUCK_BASE_ID = BASE_ID + FROG_COUNT

DUCK_LOCATION_NAMES = [f"Gako Duck {i}" for i in range(1, DUCK_COUNT + 1)]

LOCATION_NAME_TO_ID: dict[str, int] = {
    name: BASE_ID + i for i, name in enumerate(FROG_LOCATION_NAMES)
} | {name: DUCK_BASE_ID + i for i, name in enumerate(DUCK_LOCATION_NAMES)}


class MGSDeltaLocation(Location):
    game = "Metal Gear Solid Delta: Snake Eater"
