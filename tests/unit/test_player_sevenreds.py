"""TODO"""

import pytest

import casino.main
import casino.players


def test_sevenreds(monkeypatch, mock_table, mock_bet, mock_outcome):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    table = casino.main.Table()
    player = casino.players.SevenReds(table)
    player.reset(250, 100)

    assert player.stake == 100
    assert player.rounds_to_go == 250
    assert player.loss_count == 0
    assert player.bet_multiple == 1
    assert player.red_count == 7
    assert player.playing()
    assert player.place_bets() is None

    for _ in range(6):
        player.winners([mock_outcome("red", 1)])  # type: ignore
    assert player.red_count == 1
    assert player.place_bets() is None

    player.winners([mock_outcome("red", 1)])  # type: ignore
    assert player.red_count == 0
    player.place_bets()
    assert player.stake == 99

    player.lose(mock_bet("black", 1))
    assert player.loss_count == 1
    assert player.bet_multiple == 2

    player.winners([mock_outcome("black", 1)])  # type: ignore
    assert player.red_count == 7

    assert str(table.bets[0]) == "1 on red 1:1"
    with pytest.raises(IndexError):
        assert str(table.bets[1]) == "2 on red 1:1"
