"""TODO"""

# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_player_1326(monkeypatch, mock_bet, mock_table, mock_game):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    table = casino.main.Table()
    table.set_game(mock_game())
    player = casino.players.Player1326(table)
    assert not player.playing()
    player.reset(250, 100)
    assert player.playing()

    assert player.stake == 100
    assert player.rounds_to_go == 250
    assert isinstance(player.state, casino.players.Player1326NoWins)

    player.place_bets()
    player.win(table.bets[0])
    assert player.stake == 101
    assert isinstance(player.state, casino.players.Player1326OneWin)

    player.place_bets()
    player.win(table.bets[1])
    assert player.stake == 104
    assert isinstance(player.state, casino.players.Player1326TwoWins)

    player.place_bets()
    player.win(table.bets[2])
    assert player.stake == 106
    assert isinstance(player.state, casino.players.Player1326ThreeWins)

    player.place_bets()
    player.win(table.bets[3])
    assert player.stake == 112
    assert isinstance(player.state, casino.players.Player1326NoWins)

    player.place_bets()
    player.lose(table.bets[4])
    assert player.stake == 111
    assert isinstance(player.state, casino.players.Player1326NoWins)

    player.place_bets()
    player.win(table.bets[5])
    assert player.stake == 112
    assert isinstance(player.state, casino.players.Player1326OneWin)

    player.place_bets()
    player.win(table.bets[6])
    assert player.stake == 115
    assert isinstance(player.state, casino.players.Player1326TwoWins)

    player.place_bets()
    player.lose(table.bets[7])
    assert player.stake == 113
    assert isinstance(player.state, casino.players.Player1326NoWins)
