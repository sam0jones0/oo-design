"""A unit test class for the CrapsMartingale class. This test should synthesize
a fixed list of Outcome instances, Throw objects, and calls a CrapsMartingale
instance with various sequences of craps, naturals and points to assure that the
bet doubles appropriately on each loss, and is reset on each win.
"""


# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_craps_player_pass(
    monkeypatch, mock_craps_table, mock_outcome, mock_bet, mock_craps_game
):
    monkeypatch.setattr(casino.main, "CrapsTable", mock_craps_table)
    monkeypatch.setattr(casino.main, "Outcome", mock_outcome)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    monkeypatch.setattr(casino.main, "CrapsGame", mock_craps_game)
    table = casino.main.CrapsTable()
    game = mock_craps_game("dice", table)
    table.set_game(game)
    player = casino.players.CrapsMartingale(table)
    player.reset(duration=100, stake=1000)

    assert not table.bets
    if player.playing():
        player.place_bets()
    assert len(table.bets) == 1
    assert table.contains_outcome("Pass Line")
    assert player.stake == 999

    for _ in range(2):
        # Places no new bets on second run as both desired bets are already placed.
        if player.playing():
            player.place_bets()
        assert len(table.bets) == 2
        assert table.contains_outcome("Pass Odds")
        assert player.stake == 998

    for bet in table.bets:
        player.lose(bet)
    assert player.loss_count == 1
    assert player.bet_multiple == 2

    for bet in table.bets:
        player.lose(bet)
    assert player.loss_count == 2
    assert player.bet_multiple == 4

    table.bets = []

    for _ in range(2):
        if player.playing():
            player.place_bets()
    assert table.bets[0].amount == 1
    assert table.bets[1].amount == 4
    assert player.stake == 993

    for bet in table.bets:
        player.win(bet)
    assert player.loss_count == 0
    assert player.bet_multiple == 1
    assert player.stake == 1003
