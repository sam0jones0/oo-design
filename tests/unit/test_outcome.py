"""
TODO
"""

import pytest

from roulette.roulette import Outcome


def test_outcome():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Red", 1)
    o3 = Outcome("Black", 2)

    assert str(o1) == "Red 1:1"
    assert str(o3) == "Black 2:1"
    assert repr(o2) == "Outcome(name='Red', odds=1)"

    assert o1 == o2
    assert o1.odds == 1
    assert o1.name == "Red"
    assert o1 != o3
    assert o2 != o3
