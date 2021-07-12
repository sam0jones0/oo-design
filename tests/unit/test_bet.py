"""TODO"""

import pytest

from roulette.roulette import Bet, Outcome


def test_bet():
    """TODO"""
    o1 = Outcome("foo", 1)
    o2 = Outcome("bar", 4)

    b1 = Bet(1, o1)
    b2 = Bet(1, o2)

    assert b1.win_amount() == 2
    assert b2.win_amount() == 5

    assert str(b1) == "1 on foo 1:1"
    assert repr(b1) == "Bet(amount=1, outcome=Outcome(name='foo', odds=1))"
    assert str(b2) == "1 on bar 4:1"
    assert repr(b2) == "Bet(amount=1, outcome=Outcome(name='bar', odds=4))"
