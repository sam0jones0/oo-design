"""TODO"""

# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players
import tests.conftest


def test_passenger57(monkeypatch, mock_table, mock_bet):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    table = casino.main.Table()
    player = casino.players.Passenger57(table)
    assert isinstance(player.black, tests.conftest.MockOutcome)
    player.reset(250, 100)

    assert player.stake == 100
    assert player.playing()

    player.place_bets()
    player.lose(mock_bet(1, player.black, player))
    assert player.stake == 99

    player.stake = 0
    assert not player.playing()

    player.win(mock_bet(10, player.black, player))
    assert player.stake == 20
    assert player.playing()

    player.rounds_to_go = 0
    assert not player.playing()

    assert str(table.bets[0]) == "1 on red 1:1"
    with pytest.raises(IndexError):
        assert str(table.bets[1]) == "2 on red 1:1"
