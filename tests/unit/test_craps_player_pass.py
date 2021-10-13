"""A unit test class for the CrapsPlayerPass class. This test should synthesize
a fixed list of Outcome instances, Throw instances, and calls a CrapsPlayerPass
instance with various sequences of craps, naturals and points to assure that the
pass line bet is made appropriately.
"""


# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_craps_player_pass(monkeypatch, mock_craps_table, mock_outcome, mock_bet):
    monkeypatch.setattr(casino.main, "CrapsTable", mock_craps_table)
    monkeypatch.setattr(casino.main, "Outcome", mock_outcome)
    monkeypatch.setattr(casino.main, "Bet", mock_bet)
    table = casino.main.CrapsTable()
    player = casino.players.CrapsPlayerPass(table)
    player.reset(duration=100, stake=1000)

    assert not table.bets
    if player.playing():
        player.place_bets()
    assert len(table.bets) == 1
    assert table.contains_outcome("Pass Line")
    assert player.stake == 999

    if player.playing():
        player.place_bets()
    assert len(table.bets) == 1
    assert table.contains_outcome("Pass Line")
    assert player.stake == 999

    player.rounds_to_go = 0
    assert player.playing()  # Because they still have an active bet.

    player.win(table.bets[0])
    table.bets = []
    assert player.stake == 1001
    assert not player.playing()
