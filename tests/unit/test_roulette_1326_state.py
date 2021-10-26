# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_roulette_1326_state(monkeypatch, mock_bet, mock_player):
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    player = mock_player()
    state = casino.players.Roulette1326NoWins(player)
    bet = state.current_bet()
    assert state.bet_amount == 1
    assert bet.amount == 1

    state = state.next_won()
    assert isinstance(state, casino.players.Roulette1326OneWin)
    bet = state.current_bet()
    assert state.bet_amount == 3
    assert bet.amount == 3

    state = state.next_won()
    assert state.bet_amount == 2
    assert isinstance(state, casino.players.Roulette1326TwoWins)

    state = state.next_won()
    assert state.bet_amount == 6
    assert isinstance(state, casino.players.Roulette1326ThreeWins)

    state = state.next_won()
    assert state.bet_amount == 1
    assert isinstance(state, casino.players.Roulette1326NoWins)

    state = state.next_won().next_lost()
    assert state.bet_amount == 1
    assert isinstance(state, casino.players.Roulette1326NoWins)
