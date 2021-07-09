"""
TODO
"""

import pytest

from roulette.roulette import InvalidBet


def test_invalid_bet():
    with pytest.raises(InvalidBet):
        raise InvalidBet
