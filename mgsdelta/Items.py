"""
Item name/ID table + item groups for MGS Delta.

Skeleton milestone (build plan #1): a single repeatable filler item, just
enough to fill the itempool alongside the frog-only location set. The real
item pool (see README "Item pool") lands once Logic v0 (build plan #3)
starts scoping progression items against what the connector can grant.

Item IDs and location IDs (see Locations.py) each live in their own 1000-wide
range so the two tables can grow independently without renumbering.
"""

from __future__ import annotations

from BaseClasses import Item

BASE_ID = 3_900_000

FILLER_ITEM_NAME = "Ration"

ITEM_NAME_TO_ID: dict[str, int] = {
    FILLER_ITEM_NAME: BASE_ID,
}


class MGSDeltaItem(Item):
    game = "Metal Gear Solid Delta: Snake Eater"
