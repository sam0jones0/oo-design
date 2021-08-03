"""
TODO
"""

import pytest

from casino.main import InvalidBet


def test_invalid_bet():
    with pytest.raises(InvalidBet):
        raise InvalidBet
