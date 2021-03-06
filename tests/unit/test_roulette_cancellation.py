# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_roulette_cancellation(monkeypatch, mock_bet, mock_table, mock_game):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    table = casino.main.Table()
    table.set_game(mock_game())
    player = casino.players.RouletteCancellation(table)
    assert not player.playing()
    player.reset(250, 500)
    assert player.playing()

    assert player.stake == 500
    assert player.rounds_to_go == 250
    assert player.sequence == [1, 2, 3, 4, 5, 6]

    player.place_bets()
    assert player.stake == 493
    player.win(table.bets[0])
    assert player.sequence == [2, 3, 4, 5]
    assert player.stake == 507

    player.place_bets()
    assert table.bets[1].amount == 7
    player.lose(table.bets[1])
    assert player.sequence == [2, 3, 4, 5, 7]

    player.place_bets()
    player.lose(table.bets[2])
    player.place_bets()
    player.lose(table.bets[3])
    player.place_bets()
    player.lose(table.bets[3])
    player.place_bets()
    player.lose(table.bets[4])
    assert player.sequence == [2, 3, 4, 5, 7, 9, 11, 13, 15]

    player.place_bets()
    player.win(table.bets[5])
    assert player.sequence == [3, 4, 5, 7, 9, 11, 13]
    assert player.stake == 465

    player.reset_sequence()
    assert player.sequence == [1, 2, 3, 4, 5, 6]
