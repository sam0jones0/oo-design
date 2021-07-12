"""TODO"""

import pytest

from roulette.roulette import Table, Passenger57, Game, Simulator


def test_simulator(seeded_wheel):
    wheel = seeded_wheel
    table = Table()
    table.wheel = wheel
    player = Passenger57(table)
    game = Game(table, wheel)

    sim = Simulator(game, player)
    sim.init_duration = 20
    sim.samples = 20
    sim.gather()

    assert len(sim.durations) == 20
    assert len(sim.maxima) == 20
    assert len(sim.end_stakes) == 20
    assert sum(sim.durations) // sim.samples == 20
    assert sum(sim.maxima) // sim.samples == 103
    assert sum(sim.end_stakes) // sim.samples == 99
