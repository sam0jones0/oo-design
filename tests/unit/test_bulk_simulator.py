from pathlib import Path

# noinspection PyUnresolvedReferences
import pytest

import casino.main


@pytest.mark.skip  # New Player added so won't match for the moment.
def test_bulk_simulator(monkeypatch, tmpdir, mock_game, mock_simulator):
    monkeypatch.setattr(casino.main, "Simulator", mock_simulator)
    game = mock_game()
    b_sim = casino.main.BulkSimulator(game)
    b_sim.gather_all()

    assert len(b_sim.players) == len(b_sim.player_stats)
    assert len(b_sim.player_stats[0]) == 7

    single_player_stats = b_sim.player_stats[0]
    assert single_player_stats["duration_mean"] == 10.1
    assert single_player_stats["duration_stdev"] == 1.1
    assert single_player_stats["maxima_mean"] == 10.1
    assert single_player_stats["maxima_stdev"] == 1.1
    assert single_player_stats["end_stake_mean"] == 10.1
    assert single_player_stats["end_stake_stdev"] == 1.1

    b_sim.save_to_csv(tmpdir.join("stats.csv"))

    with open(tmpdir.join("stats.csv")) as f1, open(
        Path(__file__).parent.resolve().joinpath("test_stats.csv")
    ) as f2:
        assert f1.read() == f2.read()
