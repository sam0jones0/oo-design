"""
TODO
"""

import pytest
import random

from roulette.roulette import Outcome, Wheel


def test_wheel():
    """TODO"""
    rng = random.Random()
    # First randint(0, 37) with seed of 1 will return 8.
    rng.seed(1)
    wheel = Wheel(rng=rng)
    o1 = Outcome("foo", 1)
    o2 = Outcome("bar", 2)
    wheel.add_outcome(8, o1)
    wheel.add_outcome(8, o2)
    assert o1 in wheel.choose()
    assert o1 in wheel.get(8)
    assert o2 in wheel.get(8)
