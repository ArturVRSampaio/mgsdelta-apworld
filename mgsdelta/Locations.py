"""
Location name/ID table + location groups for MGS Delta.

Skeleton milestone (build plan #1): the 64 Kerotan frogs only — minimal
logic, good first milestone (see README "Location pool"). Weapon/item
pickups, Cobra Unit boss defeats, and GA doc milestones land once
mgsdelta-connector confirms it can detect them.

A location only belongs in this table once mgsdelta-connector has confirmed
it can actually detect the corresponding in-game event.
"""

from __future__ import annotations

from BaseClasses import Location

BASE_ID = 3_901_000

FROG_COUNT = 64

FROG_LOCATION_NAMES = [f"Kerotan Frog {i}" for i in range(1, FROG_COUNT + 1)]

LOCATION_NAME_TO_ID: dict[str, int] = {
    name: BASE_ID + i for i, name in enumerate(FROG_LOCATION_NAMES)
}


class MGSDeltaLocation(Location):
    game = "Metal Gear Solid Delta: Snake Eater"
