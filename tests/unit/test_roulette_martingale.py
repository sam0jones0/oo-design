"""TODO"""

# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_roulette_martingale(monkeypatch, mock_table, mock_bet, mock_game):
    monkeypatch.setattr(casino.main, "Table", mock_table)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    table = casino.main.Table()
    table.set_game(mock_game())
    player = casino.players.RouletteMartingale(table)
    player.reset(250, 100)

    assert player.stake == 100
    assert player.rounds_to_go == 250
    assert player.loss_count == 0
    assert player.bet_multiple == 1
    assert player.playing()

    player.place_bets()  # Bet starts at 10 (table minimum).
    assert player.stake == 99
    player.lose(mock_bet(1, "an_outcome", player))
    assert player.loss_count == 1
    assert player.bet_multiple == 2

    player.place_bets()  # Bet is doubled to 20.
    assert player.stake == 97
    player.lose(mock_bet(2, "an_outcome", player))
    assert player.loss_count == 2
    assert player.bet_multiple == 4

    player.place_bets()  # Bet is now 40.
    assert player.stake == 93
    player.win(mock_bet(4, "an_outcome", player))
    assert player.stake == 101
    assert player.loss_count == 0
    assert player.bet_multiple == 1

    for _ in range(10):
        player.lose(mock_bet(4, "an_outcome", player))
    player.place_bets()  # This bet_amount will exceed table.limit.

    assert str(table.bets[0]) == "1 on red 1:1"
    assert str(table.bets[1]) == "2 on red 1:1"
    assert str(table.bets[2]) == "4 on red 1:1"
    assert str(table.bets[3]) == "101 on red 1:1"  # Bet's entire remaining stake.
    with pytest.raises(IndexError):
        assert str(table.bets[4]) == "256 on red 1:1"

    table.bets = []
    assert not player.playing()