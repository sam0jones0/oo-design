"""TODO"""

from fractions import Fraction

# noinspection PyUnresolvedReferences
import pytest

import casino.main


def test_bet():
    """TODO"""
    o1 = casino.main.Outcome("foo", Fraction(2, 1))
    o2 = casino.main.Outcome("bar", Fraction(2, 3))

    buy_bet = casino.main.CommissionBet(20, o1)
    lay_bet = casino.main.CommissionBet(30, o2)

    assert buy_bet.amount == 20
    assert lay_bet.amount == 30

    assert buy_bet.price() == 21
    assert lay_bet.price() == 31

    assert buy_bet.win_amount() == 60
    assert lay_bet.win_amount() == 50

    assert str(buy_bet) == "20 on foo 2:1"
    assert (
        repr(buy_bet)
        == "CommissionBet(amount=20, outcome=Outcome(name='foo', outcome_odds=Fraction(2, 1)))"
    )
    assert str(lay_bet) == "30 on bar 2:3"
    assert (
        repr(lay_bet)
        == "CommissionBet(amount=30, outcome=Outcome(name='bar', outcome_odds=Fraction(2, 3)))"
    )
