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
from ..Items import FILLER_ITEM_NAME, MGSDeltaItem
from ..Locations import FROG_COUNT, LOCATION_NAME_TO_ID, MGSDeltaLocation
from ..Regions import VICTORY_EVENT_ITEM, VICTORY_EVENT_LOCATION
from .bases import MGSDeltaTestBase


class TestFrogSkeleton(MGSDeltaTestBase):
    options = {"progression_balancing": 0}

    def test_all_frog_locations_are_registered(self) -> None:
        self.assertEqual(FROG_COUNT, len(LOCATION_NAME_TO_ID))
        for location_name in LOCATION_NAME_TO_ID:
            location = self.multiworld.get_location(location_name, self.player)
            self.assertIsInstance(location, MGSDeltaLocation)

    def test_victory_event_is_correctly_named_and_typed(self) -> None:
        location = self.multiworld.get_location(VICTORY_EVENT_LOCATION, self.player)
        self.assertIsInstance(location, MGSDeltaLocation)
        self.assertIsInstance(location.item, MGSDeltaItem)
        self.assertEqual(VICTORY_EVENT_ITEM, location.item.name)

    def test_itempool_matches_frog_location_count(self) -> None:
        filler_items = [item for item in self.multiworld.itempool if item.name == FILLER_ITEM_NAME]
        self.assertEqual(FROG_COUNT, len(filler_items))

    def test_has_won_predicate(self) -> None:
        state = CollectionState(self.multiworld)
        self.assertFalse(Rules.has_won(state, self.player))

        victory_item = self.get_item_by_name(VICTORY_EVENT_ITEM)
        state.collect(victory_item, True)

        self.assertTrue(Rules.has_won(state, self.player))

    def test_completion_condition_is_wired_for_this_player(self) -> None:
        condition = self.multiworld.completion_condition[self.player]
        state = CollectionState(self.multiworld)
        self.assertFalse(condition(state))

        victory_item = self.get_item_by_name(VICTORY_EVENT_ITEM)
        state.collect(victory_item, True)

        self.assertTrue(condition(state))
