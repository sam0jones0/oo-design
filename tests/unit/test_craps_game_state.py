"""TODO"""

from fractions import Fraction

import pytest

import casino.main
import casino.odds
import tests.conftest


def test_craps_game_state(
    monkeypatch,
    mock_craps_game,
    mock_bet,
    mock_outcome,
    mock_player,
    override_craps_game_state_abs_methods,
):
    monkeypatch.setattr(casino.main, "Outcome", mock_outcome)
    monkeypatch.setattr(casino.main, "CrapsGame", mock_craps_game)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)

    game = casino.main.CrapsGame()
    assert isinstance(game, tests.conftest.MockCrapsGame)
    player = mock_player()
    craps_game_state = casino.main.CrapsGameState(game)  # type: ignore

    come_bet = casino.main.Bet(
        10, casino.main.Outcome("Come Line", casino.odds.PASS_COME), player
    )
    dont_come_bet = casino.main.Bet(
        20, casino.main.Outcome("Don't Come Line", casino.odds.DONT_PASS_COME), player
    )
    pass_bet = casino.main.Bet(
        30, casino.main.Outcome("Pass Line", casino.odds.PASS_COME), player
    )
    non_point_throw = casino.main.CrapsThrow(1, 2)
    point_throw = casino.main.PointThrow(5, 3)

    with pytest.raises(ValueError):
        craps_game_state.move_to_throw(come_bet, non_point_throw)
    with pytest.raises(ValueError):
        craps_game_state.move_to_throw(dont_come_bet, non_point_throw)
    with pytest.raises(ValueError):
        craps_game_state.move_to_throw(pass_bet, point_throw)

    craps_game_state.move_to_throw(come_bet, point_throw)
    assert come_bet.outcome.name == "Come Point 8"
    assert come_bet.outcome.odds == Fraction(6, 5)

    craps_game_state.move_to_throw(dont_come_bet, point_throw)
    assert dont_come_bet.outcome.name == "Don't Come Point 8"
    assert dont_come_bet.outcome.odds == Fraction(5, 6)


def test_craps_game_state_abstract_methods_reverted(monkeypatch, mock_craps_game):
    monkeypatch.setattr(casino.main, "CrapsGame", mock_craps_game)
    game = casino.main.CrapsGame()
    with pytest.raises(TypeError):
        craps_game_state = casino.main.CrapsGameState(game)
