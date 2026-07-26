"""
Skeleton milestone (build plan #1) smoke tests.

Subclassing WorldTestBase with a non-empty `options` dict opts into its
automatically-run generation/fill/reachability tests (test_fill,
test_all_state_can_reach_everything, test_empty_state_can_reach_something) —
see Archipelago's test/bases.py `run_default_tests` property.
"""

from __future__ import annotations

from BaseClasses import CollectionState

from .. import Rules
from ..Items import FILLER_ITEM_NAME
from ..Locations import FROG_COUNT, LOCATION_NAME_TO_ID
from ..Regions import VICTORY_EVENT_ITEM
from .bases import MGSDeltaTestBase


class TestFrogSkeleton(MGSDeltaTestBase):
    options = {"progression_balancing": 0}

    def test_all_frog_locations_are_registered(self) -> None:
        self.assertEqual(FROG_COUNT, len(LOCATION_NAME_TO_ID))
        for location_name in LOCATION_NAME_TO_ID:
            self.multiworld.get_location(location_name, self.player)

    def test_itempool_matches_frog_location_count(self) -> None:
        filler_items = [item for item in self.multiworld.itempool if item.name == FILLER_ITEM_NAME]
        self.assertEqual(FROG_COUNT, len(filler_items))

    def test_has_won_predicate(self) -> None:
        state = CollectionState(self.multiworld)
        self.assertFalse(Rules.has_won(state, self.player))

        victory_item = self.get_item_by_name(VICTORY_EVENT_ITEM)
        state.collect(victory_item, True)

        self.assertTrue(Rules.has_won(state, self.player))
