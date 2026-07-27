"""
Build plan #4 growth: real duck locations + the "Unlock Duck" item.

Added once mgsdelta-connector confirmed (research/NOTES.md milestone 4) it
can both detect a duck being collected and remotely trigger one via this
exact item -- see that repo for the live proof.
"""

from __future__ import annotations

from ..Items import ITEM_NAME_TO_ID, UNLOCK_DUCK_ITEM_NAME, MGSDeltaItem
from ..Locations import DUCK_COUNT, LOCATION_NAME_TO_ID, MGSDeltaLocation
from .bases import MGSDeltaTestBase


class TestDuckLocations(MGSDeltaTestBase):
    options = {"progression_balancing": 0}

    def test_all_duck_locations_are_registered(self) -> None:
        duck_location_names = [
            name for name in LOCATION_NAME_TO_ID if name.startswith("Gako Duck ")
        ]
        self.assertEqual(DUCK_COUNT, len(duck_location_names))
        for location_name in duck_location_names:
            location = self.multiworld.get_location(location_name, self.player)
            self.assertIsInstance(location, MGSDeltaLocation)

    def test_duck_location_ids_do_not_collide_with_frog_ids(self) -> None:
        ids = list(LOCATION_NAME_TO_ID.values())
        self.assertEqual(len(ids), len(set(ids)))

    def test_unlock_duck_item_is_registered(self) -> None:
        self.assertIn(UNLOCK_DUCK_ITEM_NAME, ITEM_NAME_TO_ID)

    def test_itempool_has_one_unlock_duck_item_per_duck_location(self) -> None:
        unlock_duck_items = [
            item for item in self.multiworld.itempool if item.name == UNLOCK_DUCK_ITEM_NAME
        ]
        self.assertEqual(DUCK_COUNT, len(unlock_duck_items))
        for item in unlock_duck_items:
            self.assertIsInstance(item, MGSDeltaItem)
