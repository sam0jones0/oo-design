import pytest

import casino.main


def test_invalid_bet():
    with pytest.raises(casino.main.InvalidBet):
        raise casino.main.InvalidBet
