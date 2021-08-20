"""Invoke each of the various methods that create `Outcome` instances. Only
selected `temp_bins` collections are tested which covers most cases.
"""

import pytest

import casino.main
import casino.odds
import tests.conftest


@pytest.mark.usefixtures("patched_builder")
class TestBinBuilder:
    def test_using_monkeypatched_fixtures(self):
        wheel = casino.main.Wheel()
        outcome = casino.main.Outcome("black", 1)
        assert isinstance(wheel, tests.conftest.MockWheel)
        assert isinstance(outcome, tests.conftest.MockOutcome)

    def test_correct_number_outcomes(self, patched_builder):
        builder = patched_builder
        assert len(builder.temp_bins.get(0)) == 2
        assert len(builder.temp_bins.get(1)) == 12
        assert len(builder.temp_bins.get(2)) == 14
        assert len(builder.temp_bins.get(8)) == 17
        assert len(builder.temp_bins.get(36)) == 11
        assert len(builder.temp_bins.get(37)) == 2

    def test_straight_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome(
            "Number 0", casino.odds.STRAIGHT
        ) in builder.temp_bins.get(0)
        assert casino.main.Outcome(
            "Number 00", casino.odds.STRAIGHT
        ) in builder.temp_bins.get(37)
        assert casino.main.Outcome(
            "Number 1", casino.odds.STRAIGHT
        ) in builder.temp_bins.get(1)
        assert casino.main.Outcome(
            "Number 36", casino.odds.STRAIGHT
        ) in builder.temp_bins.get(36)

    def test_split_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome(
            "1-2 Split", casino.odds.SPLIT
        ) in builder.temp_bins.get(1)
        assert casino.main.Outcome(
            "1-4 Split", casino.odds.SPLIT
        ) in builder.temp_bins.get(1)
        assert casino.main.Outcome(
            "33-36 Split", casino.odds.SPLIT
        ) in builder.temp_bins.get(36)
        assert casino.main.Outcome(
            "35-36 Split", casino.odds.SPLIT
        ) in builder.temp_bins.get(36)

    def test_street_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome(
            "1-2-3 Street", casino.odds.STREET
        ) in builder.temp_bins.get(1)
        assert casino.main.Outcome(
            "34-35-36 Street", casino.odds.STREET
        ) in builder.temp_bins.get(36)

    def test_corner_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome(
            "1-2-4-5 Corner", casino.odds.CORNER
        ) in builder.temp_bins.get(1)
        assert casino.main.Outcome(
            "1-2-4-5 Corner", casino.odds.CORNER
        ) in builder.temp_bins.get(4)
        assert casino.main.Outcome(
            "4-5-7-8 Corner", casino.odds.CORNER
        ) in builder.temp_bins.get(4)
        assert casino.main.Outcome(
            "1-2-4-5 Corner", casino.odds.CORNER
        ) in builder.temp_bins.get(5)
        assert casino.main.Outcome(
            "2-3-5-6 Corner", casino.odds.CORNER
        ) in builder.temp_bins.get(5)
        assert casino.main.Outcome(
            "4-5-7-8 Corner", casino.odds.CORNER
        ) in builder.temp_bins.get(5)
        assert casino.main.Outcome(
            "5-6-8-9 Corner", casino.odds.CORNER
        ) in builder.temp_bins.get(5)

    def test_line_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome(
            "1-2-3-4-5-6 Line", casino.odds.LINE
        ) in builder.temp_bins.get(1)
        assert casino.main.Outcome(
            "1-2-3-4-5-6 Line", casino.odds.LINE
        ) in builder.temp_bins.get(4)
        assert casino.main.Outcome(
            "4-5-6-7-8-9 Line", casino.odds.LINE
        ) in builder.temp_bins.get(4)

    def test_dozen_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome(
            "Dozen 1", casino.odds.DOZEN
        ) in builder.temp_bins.get(1)
        assert casino.main.Outcome(
            "Dozen 2", casino.odds.DOZEN
        ) in builder.temp_bins.get(17)
        assert casino.main.Outcome(
            "Dozen 3", casino.odds.DOZEN
        ) in builder.temp_bins.get(36)

    def test_column_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome(
            "Column 1", casino.odds.COLUMN
        ) in builder.temp_bins.get(1)
        assert casino.main.Outcome(
            "Column 2", casino.odds.COLUMN
        ) in builder.temp_bins.get(17)
        assert casino.main.Outcome(
            "Column 3", casino.odds.COLUMN
        ) in builder.temp_bins.get(36)

    def test_low_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome("Low", casino.odds.EVEN) in builder.temp_bins.get(1)
        assert casino.main.Outcome("Low", casino.odds.EVEN) in builder.temp_bins.get(17)
        assert casino.main.Outcome("Low", casino.odds.EVEN) in builder.temp_bins.get(18)

    def test_high_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome("High", casino.odds.EVEN) in builder.temp_bins.get(
            36
        )

    def test_red_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome("Red", casino.odds.EVEN) in builder.temp_bins.get(1)
        assert casino.main.Outcome("Red", casino.odds.EVEN) in builder.temp_bins.get(18)
        assert casino.main.Outcome("Red", casino.odds.EVEN) in builder.temp_bins.get(36)

    def test_black_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome("Black", casino.odds.EVEN) in builder.temp_bins.get(
            17
        )

    def test_even_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome("Even", casino.odds.EVEN) in builder.temp_bins.get(
            18
        )
        assert casino.main.Outcome("Even", casino.odds.EVEN) in builder.temp_bins.get(
            36
        )

    def test_odd_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome("Odd", casino.odds.EVEN) in builder.temp_bins.get(1)
        assert casino.main.Outcome("Odd", casino.odds.EVEN) in builder.temp_bins.get(17)

    def test_five_bets(self, patched_builder):
        builder = patched_builder
        assert casino.main.Outcome("Five", casino.odds.FIVE) in builder.temp_bins.get(1)
        assert casino.main.Outcome("Five", casino.odds.FIVE) in builder.temp_bins.get(0)
        assert casino.main.Outcome("Five", casino.odds.FIVE) in builder.temp_bins.get(
            37
        )
