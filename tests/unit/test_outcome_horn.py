"""TODO"""

from fractions import Fraction

import pytest

from casino.main import OutcomeHorn


def test_outcome_horn(mock_random_events):
    horn_o = OutcomeHorn("Horn", 3)

    assert str(horn_o) == "Horn (27:4, 3:1)"
    assert repr(horn_o) == "OutcomeHorn(name='Horn', odds=Fraction(3, 1))"

    assert horn_o.odds == Fraction(3, 1)
    assert horn_o.name == "Horn"

    # Test default odds used when no `RandomEvent` provided.
    assert horn_o.win_amount(10) == 30

    # Test odds change according to the provided `RandomEvent`.
    assert horn_o.win_amount(10, mock_random_events[0]) == 67
    assert horn_o.win_amount(10, mock_random_events[1]) == 30
