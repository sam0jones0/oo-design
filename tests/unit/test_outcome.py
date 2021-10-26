from fractions import Fraction

# noinspection PyUnresolvedReferences
import pytest

import casino.main


def test_outcome(mock_random_events):
    o1 = casino.main.Outcome("Red", 1)
    o2 = casino.main.Outcome("Red", 1)
    o3 = casino.main.Outcome("Black", 2)
    o4 = casino.main.Outcome("Craps", Fraction(6, 5))

    assert str(o1) == "Red 1:1"
    assert str(o3) == "Black 2:1"
    assert repr(o2) == "Outcome(name='Red', outcome_odds=Fraction(1, 1))"
    assert str(o4) == "Craps 6:5"
    assert repr(o4) == "Outcome(name='Craps', outcome_odds=Fraction(6, 5))"

    assert o1 == o2
    assert o1.odds == Fraction(1, 1)
    assert o3.odds == Fraction(2, 1)
    assert o1.name == "Red"
    assert o1 != o3
    assert o2 != o3

    assert o1.win_amount(10) == 10
    assert o1.win_amount(10, mock_random_events[0]) == 10
    assert o3.win_amount(10) == 20
    assert o3.win_amount(10, mock_random_events[1]) == 20
    assert o4.win_amount(10) == 12
