"""TODO"""

import pytest

import casino.main


def test_craps_table():
    """TODO"""
    game = casino.main.CrapsGame()
    table = casino.main.CrapsTable(game)

    field_bet = casino.main.Bet(1, casino.main.Outcome("Field", 1))
    pass_bet = casino.main.Bet(5, casino.main.Outcome("Pass", 1))

    # Only 'Pass' and 'Don't Pass' bets are valid when point is off.
    assert not table.is_valid_bet(field_bet)
    assert table.is_valid_bet(pass_bet)

    # All bets are valid when point is on.
    game.current_point = 6
    assert table.is_valid_bet(field_bet)
    assert table.is_valid_bet(pass_bet)

    table.place_bet(field_bet)
    table.place_bet(pass_bet)
    assert table.validate()

    game.current_point = None
    assert not table.validate()

    oversize_bet = casino.main.Bet(99999, casino.main.Outcome("Field", 1))
    with pytest.raises(casino.main.InvalidBet):
        table.place_bet(oversize_bet)
