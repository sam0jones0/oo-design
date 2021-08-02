"""TODO"""

import pytest

import casino.roulette
from casino.roulette import (
    Player1326State,
    Player1326NoWins,
    Player1326OneWin,
    Player1326TwoWins,
    Player1326ThreeWins,
)


def test_player1326state(monkeypatch, mock_bet, mock_player):
    monkeypatch.setattr(casino.roulette, "Bet", mock_bet)
    player = mock_player()
    state = Player1326NoWins(player)
    bet = state.current_bet()
    assert state.bet_amount == 1
    assert bet.amount == 1

    state = state.next_won()
    assert isinstance(state, Player1326OneWin)
    bet = state.current_bet()
    assert state.bet_amount == 3
    assert bet.amount == 3

    state = state.next_won()
    assert state.bet_amount == 2
    assert isinstance(state, Player1326TwoWins)

    state = state.next_won()
    assert state.bet_amount == 6
    assert isinstance(state, Player1326ThreeWins)

    state = state.next_won()
    assert state.bet_amount == 1
    assert isinstance(state, Player1326NoWins)

    state = state.next_won().next_lost()
    assert state.bet_amount == 1
    assert isinstance(state, Player1326NoWins)
