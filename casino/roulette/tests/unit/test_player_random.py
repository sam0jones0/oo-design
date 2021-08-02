"""TODO"""
import random

import pytest

import casino.roulette
from casino.roulette import PlayerRandom


def test_martingale(monkeypatch, mock_table, mock_bet):
    monkeypatch.setattr(casino.roulette, "Table", mock_table)
    monkeypatch.setattr(casino.roulette, "Bet", mock_bet)
    table = casino.roulette.Table()
    player = PlayerRandom(table)
    player.rng = random.Random()
    player.rng.seed(1)
    player.reset(250, 100)

    for _ in range(5):
        player.place_bets()
    assert player.stake == 95
    player.lose(mock_bet(1, "an_outcome"))
    assert player.playing()

    player.stake = 0
    assert not player.playing()

    player.win(mock_bet(10, "an_outcome"))
    assert player.stake == 20
    assert player.playing()

    player.rounds_to_go = 0
    assert not player.playing()

    assert str(table.bets[0]) == "1 on Red 1:1"
    assert str(table.bets[1]) == "1 on Dozen 1 6:1"
    assert str(table.bets[2]) == "1 on Red 1:1"
    assert str(table.bets[3]) == "1 on 4-1 Split 4:1"
    assert str(table.bets[4]) == "1 on Red 1:1"
    with pytest.raises(IndexError):
        assert str(table.bets[5]) == "1 on Red 1:1"
