"""
Archipelago world definition for Metal Gear Solid Delta: Snake Eater.

This package is meant to be dropped into an Archipelago checkout's `worlds/`
directory (or packaged as `mgsdelta.apworld`) — see the repo README for the
full build plan. Nothing here talks to the game; that's `mgsdelta-connector`'s job.
"""

from __future__ import annotations

from BaseClasses import ItemClassification
from worlds.AutoWorld import WebWorld, World

from . import Regions, Rules
from .Items import FILLER_ITEM_NAME, ITEM_NAME_TO_ID, UNLOCK_DUCK_ITEM_NAME, MGSDeltaItem
from .Locations import DUCK_COUNT, LOCATION_NAME_TO_ID


class MGSDeltaWebWorld(WebWorld):
    """WebHost display config. Setup guide/game info docs land before any upstream submission."""

    game = "Metal Gear Solid Delta: Snake Eater"
    theme = "ocean"


class MGSDeltaWorld(World):
    """Archipelago world for Metal Gear Solid Delta: Snake Eater.

    Skeleton milestone (build plan #1): registers the world with a
    frog-only location set and no traversal logic yet. Build plan #4
    growth: real duck locations plus a real, connector-grantable
    "Unlock Duck" item, one per duck location.
    """

    game = "Metal Gear Solid Delta: Snake Eater"
    web = MGSDeltaWebWorld()

    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    def create_regions(self) -> None:
        Regions.create_regions(self)

    def set_rules(self) -> None:
        Rules.set_rules(self)

    def create_items(self) -> None:
        unfilled_count = len(self.multiworld.get_unfilled_locations(self.player))
        duck_item_count = min(DUCK_COUNT, unfilled_count)
        filler_count = unfilled_count - duck_item_count
        items = [self.create_item(UNLOCK_DUCK_ITEM_NAME) for _ in range(duck_item_count)]
        items += [self.create_item(FILLER_ITEM_NAME) for _ in range(filler_count)]
        self.multiworld.itempool += items

    def create_item(self, name: str) -> MGSDeltaItem:
        item_id = self.item_name_to_id[name]
        return MGSDeltaItem(name, ItemClassification.filler, item_id, self.player)
