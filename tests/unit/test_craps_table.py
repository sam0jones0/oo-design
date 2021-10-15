"""TODO"""

import pytest

import casino.main


def test_craps_table(mock_player):
    """TODO"""
    table = casino.main.Table()
    game = casino.main.CrapsGame("dice", table)  # type: ignore
    player = mock_player()

    field_bet = casino.main.Bet(1, casino.main.Outcome("Field", 1), player)
    pass_bet = casino.main.Bet(5, casino.main.Outcome("Pass Line", 1), player)

    with pytest.raises(AttributeError):
        table.place_bet(pass_bet)
    table.set_game(game)
    table.place_bet(pass_bet)

    # Only 'Pass' and 'Don't Pass' bets are valid when point is off.
    with pytest.raises(casino.main.InvalidBet):
        table.place_bet(field_bet)

    assert len(table.bets) == 1
    assert table.bets_total == 5
    table.validate()

    game.state = casino.main.CrapsGamePointOn(4, game)
    with pytest.raises(casino.main.InvalidBet):
        table.place_bet(pass_bet)
    table.place_bet(field_bet)

    assert len(table.bets) == 2
    assert table.bets_total == 6
    table.validate()

    oversize_bet = casino.main.Bet(99999, casino.main.Outcome("Field", 1), player)
    with pytest.raises(casino.main.InvalidBet):
        table.place_bet(oversize_bet)
