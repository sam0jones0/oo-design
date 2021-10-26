import random

import pytest

import casino.main
import casino.players


def test_roulette_random(monkeypatch, mock_table, mock_bet, mock_game):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    table = casino.main.Table()
    table.set_game(mock_game())
    player = casino.players.RouletteRandom(table)
    player.rng = random.Random()
    player.rng.seed(1)
    player.reset(250, 100)

    for _ in range(5):
        player.place_bets()
    assert player.stake == 95
    player.lose(mock_bet(1, "an_outcome", player))
    assert player.playing()

    player.stake = 0
    assert player.playing()  # Because there are still active bets.

    player.win(mock_bet(10, "an_outcome", player))
    assert player.stake == 20
    assert player.playing()

    assert str(table.bets[0]) == "1 on Red 1:1"
    assert str(table.bets[1]) == "1 on Dozen 1 6:1"
    assert str(table.bets[2]) == "1 on Red 1:1"
    assert str(table.bets[3]) == "1 on 4-1 Split 4:1"
    assert str(table.bets[4]) == "1 on Red 1:1"
    with pytest.raises(IndexError):
        assert str(table.bets[5]) == "1 on Red 1:1"

    player.rounds_to_go = 0
    table.bets = []
    assert not player.playing()
