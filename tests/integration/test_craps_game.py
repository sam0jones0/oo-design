"""Performs a demonstration of the CrapsGame class. This demo
program creates the Dice object, the stub CrapsPlayer object, and the
Table object. It creates the CrapsGame object and cycles a few times.
Note that we will need to configure the Dice object to return non-random
results.
"""

# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_craps_game(seeded_dice):
    dice = seeded_dice
    table = casino.main.Table()
    game = casino.main.CrapsGame(dice, table)
    table.set_game(game)
    player = casino.players.CrapsPass(table)
    player.reset(duration=50, stake=100)
    assert player.stake == 100

    game.cycle(player)  # Rolls (5, 2)
    assert player.stake == 101
    assert player.rounds_to_go == 49
    assert str(game.state) == "The Point Is Off"
    assert len(table.bets) == 0
    assert table.bets_total == 0

    game.cycle(player)  # Rolls (4, 3)
    assert player.stake == 102
    assert player.rounds_to_go == 48
    assert str(game.state) == "The Point Is Off"
    assert len(table.bets) == 0
    assert table.bets_total == 0

    game.cycle(player)  # Rolls (3, 5)
    assert player.stake == 101
    assert player.rounds_to_go == 47
    assert str(game.state) == "The Point Is 8"
    assert len(table.bets) == 1
    assert table.bets_total == 1

    game.cycle(player)  # Rolls (3, 3)
    assert player.stake == 101
    assert player.rounds_to_go == 46
    assert str(game.state) == "The Point Is 8"

    game.cycle(player)  # Rolls (4, 6)
    assert player.stake == 101
    assert player.rounds_to_go == 45
    assert str(game.state) == "The Point Is 8"

    game.cycle(player)  # Rolls (2, 6)
    assert player.stake == 103
    assert player.rounds_to_go == 44
    assert str(game.state) == "The Point Is Off"
