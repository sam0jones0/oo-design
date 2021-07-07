"""TODO"""

import pytest

import roulette
from roulette.roulette import Passenger57


def test_passenger57(monkeypatch, mock_table, mock_bet):
    monkeypatch.setattr(roulette.roulette, "Table", mock_table)
    monkeypatch.setattr(roulette.roulette, "Bet", mock_bet)
    table = roulette.roulette.Table()
    player = Passenger57(table)

    assert player.stake == 1000
    assert player.playing()

    player.place_bets()
    player.lose(mock_bet(10, player.black))
    assert player.stake == 990

    player.stake = 0
    assert not player.playing()

    player.win(mock_bet(100, player.black))
    assert player.stake == 200
    assert player.playing()

    player.rounds_to_go = 0
    assert not player.playing()
