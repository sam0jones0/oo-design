# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players
import tests.conftest


def test_player(monkeypatch, mock_table, mock_bet, override_player_abstract_methods):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    table = casino.main.Table()
    player = casino.players.Player(table)

    assert isinstance(player.table, tests.conftest.MockTable)
    assert player.stake == 0
    assert player.rounds_to_go == 0
    assert not player.playing()

    player.reset(250, 100)
    assert player.stake == 100
    assert player.rounds_to_go == 250
    assert player.playing()

    assert player.place_bets() == player.place_bets()

    player.win(mock_bet(50, "an_outcome", player))
    assert player.stake == 200

    assert player.lose(mock_bet(50, "an_outcome", player)) is None
    assert player.winners("outcome_set") is None  # type: ignore


def test_player_abstract_methods_reverted(monkeypatch, mock_table):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    table = casino.main.Table()
    with pytest.raises(TypeError):
        player = casino.players.Player(table)
