"""
TODO
"""

import pytest

from roulette.roulette import BinBuilder, Game, Passenger57, Table

# FIXME
def test_game(mock_wheel):
    wheel = mock_wheel()
    BinBuilder().build_bins(wheel)
    table = Table()
    player = Passenger57(table)
    game = Game(table, wheel)
    for _ in range(3):
        game.cycle(player)

    assert game.table.bets == []

