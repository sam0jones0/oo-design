"""
TODO
"""

import pytest

from roulette.roulette import Bin, Outcome


def test_bin_construction():
    """TODO"""
    five = Outcome("00-0-1-2-3", 6)
    zero = Bin(Outcome("0", 35), five)
    zero_zero = Bin(Outcome("00", 35))
    zero_zero.add(five)
    assert five in zero
    assert five in zero_zero
    assert isinstance(zero, Bin)
    assert isinstance(zero_zero, Bin)
    assert isinstance(zero_zero.outcomes, frozenset)

