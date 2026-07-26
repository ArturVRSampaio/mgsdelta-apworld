"""Smoke test proving the test/coverage/CI harness actually runs end to end."""

import mgsdelta


def test_package_is_importable() -> None:
    assert mgsdelta is not None
