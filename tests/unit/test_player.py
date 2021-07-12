"""TODO"""

import pytest

import roulette
from roulette.roulette import Player
from tests.conftest import MockTable


def test_player(monkeypatch, mock_table, mock_bet):
    monkeypatch.setattr(roulette.roulette, "Table", mock_table)
    table = roulette.roulette.Table()
    player = Player(table)

    assert isinstance(player.table, MockTable)
    assert player.stake == 0
    assert player.rounds_to_go == 0
    assert not player.playing()

    player.reset(250, 1000)
    assert player.stake == 1000
    assert player.rounds_to_go == 250
    assert player.playing()

    with pytest.raises(NotImplementedError):
        player.place_bets()

    player.win(mock_bet(500, "an_outcome"))
    assert player.stake == 2000

    assert player.lose(mock_bet(500, "an_outcome")) is None
    assert player.winners("outcome_set") is None  # type: ignore
