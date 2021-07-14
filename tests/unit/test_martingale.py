"""TODO"""

import pytest

import roulette
from roulette.roulette import Martingale


def test_martingale(monkeypatch, mock_table, mock_bet):
    monkeypatch.setattr(roulette.roulette, "Table", mock_table)
    monkeypatch.setattr(roulette.roulette, "Bet", mock_bet)
    table = roulette.roulette.Table()
    player = Martingale(table)
    player.reset(250, 100)

    assert player.stake == 100
    assert player.rounds_to_go == 250
    assert player.loss_count == 0
    assert player.bet_multiple == 1
    assert player.playing()

    player.place_bets()  # Bet starts at 10 (table minimum).
    assert player.stake == 99
    player.lose(mock_bet(1, "an_outcome"))
    assert player.loss_count == 1
    assert player.bet_multiple == 2

    player.place_bets()  # Bet is doubled to 20.
    assert player.stake == 97
    player.lose(mock_bet(2, "an_outcome"))
    assert player.loss_count == 2
    assert player.bet_multiple == 4

    player.place_bets()  # Bet is now 40.
    assert player.stake == 93
    player.win(mock_bet(4, "an_outcome"))
    assert player.stake == 101
    assert player.loss_count == 0
    assert player.bet_multiple == 1

    for _ in range(10):
        player.lose(mock_bet(4, "an_outcome"))
    player.place_bets()  # This bet_amount will exceed table.limit.
    assert not player.playing()

    assert str(table.bets[0]) == "1 on red 1:1"
    assert str(table.bets[1]) == "2 on red 1:1"
    assert str(table.bets[2]) == "4 on red 1:1"
    with pytest.raises(IndexError):
        assert str(table.bets[3]) == "128 on red 1:1"
