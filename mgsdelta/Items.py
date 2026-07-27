"""
Item name/ID table + item groups for MGS Delta.

Skeleton milestone (build plan #1): a single repeatable filler item, just
enough to fill the itempool alongside the frog-only location set. Build
plan #4 growth: "Unlock Duck", a real item mgsdelta-connector can actually
grant (see that repo's research/NOTES.md milestone 4 -- it remotely
triggers GakoSetCollected() on an uncollected duck in-game). The rest of
the real item pool (see README "Item pool") lands once Logic v0 (build
plan #3) starts scoping progression items against what the connector can
grant.

Item IDs and location IDs (see Locations.py) each live in their own 1000-wide
range so the two tables can grow independently without renumbering.
"""

from __future__ import annotations

from BaseClasses import Item

BASE_ID = 3_900_000

FILLER_ITEM_NAME = "Ration"

UNLOCK_DUCK_ITEM_NAME = "Unlock Duck"

ITEM_NAME_TO_ID: dict[str, int] = {
    FILLER_ITEM_NAME: BASE_ID,
    UNLOCK_DUCK_ITEM_NAME: BASE_ID + 1,
}


class MGSDeltaItem(Item):
    game = "Metal Gear Solid Delta: Snake Eater"
