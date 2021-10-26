# noinspection PyUnresolvedReferences
import pytest

import casino.main


def test_bet(mock_player):
    player = mock_player()
    o1 = casino.main.Outcome("foo", 1)
    o2 = casino.main.Outcome("bar", 4)

    b1 = casino.main.Bet(1, o1, player)
    b2 = casino.main.Bet(1, o2, player)

    assert b1.amount == b1.price() == 1
    assert b2.amount == b2.price() == 1

    assert b1.win_amount() == 2
    assert b2.win_amount() == 5

    assert str(b1) == "1 on foo 1:1"
    assert (
        repr(b1)
        == "Bet(amount=1, outcome=Outcome(name='foo', outcome_odds=Fraction(1, 1)), player=MockPlayer())"
    )
    assert str(b2) == "1 on bar 4:1"
    assert (
        repr(b2)
        == "Bet(amount=1, outcome=Outcome(name='bar', outcome_odds=Fraction(4, 1)), player=MockPlayer())"
    )
