"""
TODO
"""

# noinspection PyUnresolvedReferences
import pytest

import casino.main


def test_bin_construction():
    """TODO"""
    five = casino.main.Outcome("00-0-1-2-3", 6)

    zero = casino.main.Bin()
    zero.add([casino.main.Outcome("0", 35), five])
    assert zero.event_id is None

    zero_zero = casino.main.Bin()
    zero_zero.add([casino.main.Outcome("00", 35)])
    zero_zero.add([five])

    assert five in zero
    assert five in zero_zero
    assert isinstance(zero, casino.main.Bin)
    assert isinstance(zero_zero, casino.main.Bin)
    assert isinstance(zero_zero.outcomes, frozenset)

    bin_iter = iter(zero)
    assert isinstance(next(bin_iter), casino.main.Outcome)
