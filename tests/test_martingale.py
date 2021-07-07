"""TODO"""

import pytest

import roulette
from roulette.roulette import Martingale


def test_martingale(monkeypatch, mock_table, mock_bet):
    monkeypatch.setattr(roulette.roulette, "Table", mock_table)
    monkeypatch.setattr(roulette.roulette, "Bet", mock_bet)
    table = roulette.roulette.Table()
    player = Martingale(table)

    assert player.stake == 1000
    assert player.rounds_to_go == 20
    assert player.loss_count == 0
    assert player.bet_multiple == 1
    assert player.playing()

    player.place_bets()  # Bet starts at 10 (table minimum).
    assert player.stake == 990
    player.lose(mock_bet(10, "an_outcome"))
    assert player.loss_count == 1
    assert player.bet_multiple == 2

    player.place_bets()  # Bet is doubled to 20.
    assert player.stake == 970
    player.lose(mock_bet(20, "an_outcome"))
    assert player.loss_count == 2
    assert player.bet_multiple == 4

    player.place_bets()  # Bet is now 40.
    assert player.stake == 930
    player.win(mock_bet(40, "an_outcome"))
    assert player.stake == 1010
    assert player.loss_count == 0
    assert player.bet_multiple == 1

    player.stake = 0
    assert not player.playing()
