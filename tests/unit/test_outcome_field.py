"""TODO"""

from fractions import Fraction

# noinspection PyUnresolvedReferences
import pytest

import casino.main


def test_outcome_field(mock_random_events):
    field_o = casino.main.OutcomeField("Field", 1)

    assert str(field_o) == "Field (1:1, 2 and 12 2:1)"
    assert repr(field_o) == "OutcomeField(name='Field', outcome_odds=Fraction(1, 1))"

    assert field_o.odds == Fraction(1, 1)
    assert field_o.name == "Field"

    # Test default odds used when no `RandomEvent` provided.
    assert field_o.win_amount(10) == 10

    # Test odds change according to the provided `RandomEvent`.
    assert field_o.win_amount(10, mock_random_events[0]) == 20
    assert field_o.win_amount(10, mock_random_events[1]) == 10
