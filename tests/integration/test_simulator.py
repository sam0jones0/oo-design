"""TODO"""

# noinspection PyUnresolvedReferences
import pytest

import casino.main
import casino.players


def test_simulator(seeded_wheel):
    wheel = seeded_wheel
    table = casino.main.Table()
    table.set_game(casino.main.RouletteGame(table, wheel))
    table.game.wheel = wheel
    player = casino.players.Passenger57(table)
    game = casino.main.RouletteGame(table, wheel)

    sim = casino.main.Simulator(game, player)
    sim.init_duration = 20
    sim.samples = 20
    sim.gather()

    assert len(sim.durations) == 20
    assert len(sim.maxima) == 20
    assert len(sim.end_stakes) == 20
    assert sum(sim.durations) // sim.samples == 20
    assert sum(sim.maxima) // sim.samples == 103
    assert sum(sim.end_stakes) // sim.samples == 99
