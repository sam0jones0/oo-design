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
    o3 = Outcome("har", 3)

    wheel.add_outcomes(8, [o1])
    wheel.add_outcomes(8, [o2, o3])
    random_bin = wheel.choose()  # Will return bin 8.

    assert o1 in random_bin
    assert o1 in wheel.get_bin(8)
    assert o2 in random_bin
    assert o3 in wheel.get_bin(8)

    assert len(wheel.all_outcomes) == 3

    assert wheel.get_outcome(o1.name) is o1
    assert wheel.get_outcome(o2.name) is o2
    assert wheel.get_outcome(o3.name) is o3

    with pytest.raises(KeyError) as exc_info:
        wheel.get_outcome("does_not_exist")
    exception_msg = exc_info.value.args[0]
    assert exception_msg == "No Outcome with name: does_not_exist"
