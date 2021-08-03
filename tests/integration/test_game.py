"""
TODO
"""

import pytest

from casino.main import BinBuilder, Game, Passenger57, Table


def test_game(seeded_wheel):
    """Integration test of `Game` using the simple player `Passenger57`, who always
    bets on black.

    A non-random seeded wheel is used and will choose the following 20 bins:
    [8, 36, 4, 16, 7, 31, 28, 30, 24, 13, 6, 31, 1, 24, 27, 0, 28, 17, 14, 37]
    """
    wheel = seeded_wheel
    table = Table()
    table.wheel = wheel
    player = Passenger57(table)  # Always bets 1 on black.
    player.reset(20, 100)
    game = Game(table, wheel)

    while player.playing():
        game.cycle(player)

    # Total of 11/20 winning bins: 8, 4, 31, 28, 24, 13, 6, 31, 24, 28, 17
    assert player.rounds_to_go == 0
    assert player.stake == 102
    assert game.table.bets == []  # Check table has been cleared.
