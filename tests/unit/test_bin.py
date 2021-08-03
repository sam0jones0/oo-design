"""
TODO
"""

import pytest

from casino.main import Bin, Outcome


def test_bin_construction():
    """TODO"""
    five = Outcome("00-0-1-2-3", 6)

    zero = Bin()
    zero.add([Outcome("0", 35), five])

    zero_zero = Bin()
    zero_zero.add([Outcome("00", 35)])
    zero_zero.add([five])

    assert five in zero
    assert five in zero_zero
    assert isinstance(zero, Bin)
    assert isinstance(zero_zero, Bin)
    assert isinstance(zero_zero.outcomes, frozenset)

    bin_iter = iter(zero)
    assert isinstance(next(bin_iter), Outcome)
