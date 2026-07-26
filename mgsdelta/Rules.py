"""
Access rules (region entrances + location requirements) for MGS Delta.

Skeleton milestone (build plan #1): no access rules yet — all 64 frogs sit
in a single reachable region with no gating (see Regions.py). The only rule
wired here is the placeholder completion condition (collect the Victory
event, which is always immediately reachable). Real rules like "reaching
The End's fight requires thermal goggles" or "opening storage door X
requires key item Y" land with Logic v0 (build plan #3), kept 1:1 with what
mgsdelta-connector can actually verify a player owns at runtime.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState

from .Regions import VICTORY_EVENT_ITEM

if TYPE_CHECKING:
    from . import MGSDeltaWorld


def has_won(state: CollectionState, player: int) -> bool:
    """Pure predicate: has this player collected the skeleton milestone's Victory event item?"""
    return bool(state.has(VICTORY_EVENT_ITEM, player))


def set_rules(world: MGSDeltaWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: has_won(state, world.player)
