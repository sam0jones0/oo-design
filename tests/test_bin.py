"""
TODO
"""

import pytest

from roulette.roulette import Bin, Outcome


def test_bin_construction():
    assert issubclass(Bin, frozenset)
    five = Outcome("00-0-1-2-3", 6)
    zero = Bin({Outcome("0", 35), five})
    zero_zero = Bin({Outcome("00", 35), five})
    assert five in zero
    assert five in zero_zero
    assert isinstance(zero, Bin)
    assert isinstance(zero_zero, Bin)


@pytest.mark.parametrize("param", [10, None, Outcome("0", 35)])
def test_bin_error_on_non_iterable(param):
    with pytest.raises(TypeError):
        Bin(param)  # type: ignore
