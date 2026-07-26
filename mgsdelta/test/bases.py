"""Shared Archipelago TestBase for MGS Delta world tests."""

from __future__ import annotations

from test.bases import WorldTestBase

from .. import MGSDeltaWorld


class MGSDeltaTestBase(WorldTestBase):
    game = "Metal Gear Solid Delta: Snake Eater"
    world: MGSDeltaWorld
