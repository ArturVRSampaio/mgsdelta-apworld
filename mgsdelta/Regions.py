"""
Region graph for MGS Delta.

Skeleton milestone (build plan #1): a single "Menu" region holding all 64
frog locations plus the placeholder Victory event — no traversal logic yet.
The real chapter-by-chapter graph (see README "Regions & logic")

    Dolinovodno -> Ravine -> Bolshaya Past forest -> Ponizovje swamp
        -> Groznyj Grad -> Volgin's chapters -> credits

lands with Region graph v0 (build plan #2), built from a documented
playthrough, not guesswork.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .Items import MGSDeltaItem
from .Locations import LOCATION_NAME_TO_ID, MGSDeltaLocation

if TYPE_CHECKING:
    from . import MGSDeltaWorld

VICTORY_EVENT_LOCATION = "All Frogs Sighted"
VICTORY_EVENT_ITEM = "Victory"


def create_regions(world: MGSDeltaWorld) -> None:
    menu = Region(world.origin_region_name, world.player, world.multiworld)
    menu.add_locations(LOCATION_NAME_TO_ID, MGSDeltaLocation)
    menu.add_event(
        VICTORY_EVENT_LOCATION,
        VICTORY_EVENT_ITEM,
        location_type=MGSDeltaLocation,
        item_type=MGSDeltaItem,
    )
    world.multiworld.regions.append(menu)
