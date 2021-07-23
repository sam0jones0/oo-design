"""TODO"""

import pytest

import roulette
from roulette.roulette import PlayerFibonacci


def test_player_fibonacci(monkeypatch, mock_table, mock_bet):
    monkeypatch.setattr(roulette.roulette, "Table", mock_table)
    monkeypatch.setattr(roulette.roulette, "Bet", mock_bet)
    table = roulette.roulette.Table()
    player = PlayerFibonacci(table)
    player.reset(250, 100)

    assert player.stake == 100
    assert player.rounds_to_go == 250
    assert player.recent == 1
    assert player.previous == 0
    assert player.playing()

    player.place_bets()
    assert player.stake == 99
    player.lose(table.bets[-1])

    player.place_bets()
    assert player.stake == 98
    player.lose(table.bets[-1])

    player.place_bets()
    assert player.stake == 96
    player.lose(table.bets[-1])

    assert player.recent == 3
    assert player.previous == 2
    player.place_bets()
    assert table.bets[-1].amount == 3
    player.win(table.bets[-1])
    assert player.recent == 1
    assert player.previous == 0
    assert player.stake == 99

    for _ in range(11):
        player.lose(table.bets[3])
    assert player.recent == 144
    assert player.previous == 89
    player.place_bets()
    assert table.bets[-1].amount == 99

    assert player.stake == 0
    assert not player.playing()