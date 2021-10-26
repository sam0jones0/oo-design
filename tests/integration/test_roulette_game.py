# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_game(seeded_wheel):
    """Integration test of `Game` using the simple player `Passenger57`, who always
    bets on black.

    A non-random seeded wheel is used and will choose the following 20 bins:
    [8, 36, 4, 16, 7, 31, 28, 30, 24, 13, 6, 31, 1, 24, 27, 0, 28, 17, 14, 37]
    """
    wheel = seeded_wheel
    table = casino.main.Table()
    game = casino.main.RouletteGame(wheel, table)
    table.set_game(game)
    player = casino.players.RouletteMartingale(table)
    player.reset(20, 100)

    while player.playing():
        game.cycle(player)

    assert player.rounds_to_go == 0
    assert player.stake == 108
    assert game.table.bets == []  # Check table has been cleared.
