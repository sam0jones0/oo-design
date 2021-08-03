"""TODO"""

import pytest

import casino.main
from casino.main import Player
from tests.conftest import MockTable


def test_player(monkeypatch, mock_table, mock_bet):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    table = casino.main.Table()
    player = Player(table)

    assert isinstance(player.table, MockTable)
    assert player.stake == 0
    assert player.rounds_to_go == 0
    assert not player.playing()

    player.reset(250, 100)
    assert player.stake == 100
    assert player.rounds_to_go == 250
    assert player.playing()

    with pytest.raises(NotImplementedError):
        player.place_bets()

    player.win(mock_bet(50, "an_outcome"))
    assert player.stake == 200

    assert player.lose(mock_bet(50, "an_outcome")) is None
    assert player.winners("outcome_set") is None  # type: ignore
