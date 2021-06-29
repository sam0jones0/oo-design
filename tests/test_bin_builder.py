"""Invoke each of the various methods that create `Outcome` instances. Only
selected `temp_bins` collections are tested which covers most cases.
"""

import pytest

from roulette import odds
from roulette.roulette import Outcome


def test_correct_number_outcomes(built_builder):
    builder = built_builder
    assert len(builder.temp_bins.get(0)) == 2
    assert len(builder.temp_bins.get(1)) == 12
    assert len(builder.temp_bins.get(2)) == 14
    assert len(builder.temp_bins.get(8)) == 17
    assert len(builder.temp_bins.get(36)) == 11
    assert len(builder.temp_bins.get(37)) == 2


def test_straight_bets(built_builder):
    builder = built_builder
    assert Outcome("Number 0", odds.STRAIGHT) in builder.temp_bins.get(0)
    assert Outcome("Number 00", odds.STRAIGHT) in builder.temp_bins.get(37)
    assert Outcome("Number 1", odds.STRAIGHT) in builder.temp_bins.get(1)
    assert Outcome("Number 36", odds.STRAIGHT) in builder.temp_bins.get(36)


def test_split_bets(built_builder):
    builder = built_builder
    assert Outcome("1-2 Split", odds.SPLIT) in builder.temp_bins.get(1)
    assert Outcome("1-4 Split", odds.SPLIT) in builder.temp_bins.get(1)
    assert Outcome("33-36 Split", odds.SPLIT) in builder.temp_bins.get(36)
    assert Outcome("35-36 Split", odds.SPLIT) in builder.temp_bins.get(36)


def test_street_bets(built_builder):
    builder = built_builder
    assert Outcome("1-2-3 Street", odds.STREET) in builder.temp_bins.get(1)
    assert Outcome("34-35-36 Street", odds.STREET) in builder.temp_bins.get(36)


def test_corner_bets(built_builder):
    builder = built_builder
    assert Outcome("1-2-4-5 Corner", odds.CORNER) in builder.temp_bins.get(1)
    assert Outcome("1-2-4-5 Corner", odds.CORNER) in builder.temp_bins.get(4)
    assert Outcome("4-5-7-8 Corner", odds.CORNER) in builder.temp_bins.get(4)
    assert Outcome("1-2-4-5 Corner", odds.CORNER) in builder.temp_bins.get(5)
    assert Outcome("2-3-5-6 Corner", odds.CORNER) in builder.temp_bins.get(5)
    assert Outcome("4-5-7-8 Corner", odds.CORNER) in builder.temp_bins.get(5)
    assert Outcome("5-6-8-9 Corner", odds.CORNER) in builder.temp_bins.get(5)


def test_line_bets(built_builder):
    builder = built_builder
    assert Outcome("1-2-3-4-5-6 Line", odds.LINE) in builder.temp_bins.get(1)
    assert Outcome("1-2-3-4-5-6 Line", odds.LINE) in builder.temp_bins.get(4)
    assert Outcome("4-5-6-7-8-9 Line", odds.LINE) in builder.temp_bins.get(4)


def test_dozen_bets(built_builder):
    builder = built_builder
    assert Outcome("Dozen 1", odds.DOZEN) in builder.temp_bins.get(1)
    assert Outcome("Dozen 2", odds.DOZEN) in builder.temp_bins.get(17)
    assert Outcome("Dozen 3", odds.DOZEN) in builder.temp_bins.get(36)


def test_column_bets(built_builder):
    builder = built_builder
    assert Outcome("Column 1", odds.COLUMN) in builder.temp_bins.get(1)
    assert Outcome("Column 2", odds.COLUMN) in builder.temp_bins.get(17)
    assert Outcome("Column 3", odds.COLUMN) in builder.temp_bins.get(36)


def test_low_bets(built_builder):
    builder = built_builder
    assert Outcome("Low", odds.EVEN) in builder.temp_bins.get(1)
    assert Outcome("Low", odds.EVEN) in builder.temp_bins.get(17)
    assert Outcome("Low", odds.EVEN) in builder.temp_bins.get(18)


def test_high_bets(built_builder):
    builder = built_builder
    assert Outcome("High", odds.EVEN) in builder.temp_bins.get(36)


def test_red_bets(built_builder):
    builder = built_builder
    assert Outcome("Red", odds.EVEN) in builder.temp_bins.get(1)
    assert Outcome("Red", odds.EVEN) in builder.temp_bins.get(18)
    assert Outcome("Red", odds.EVEN) in builder.temp_bins.get(36)


def test_black_bets(built_builder):
    builder = built_builder
    assert Outcome("Black", odds.EVEN) in builder.temp_bins.get(17)


def test_even_bets(built_builder):
    builder = built_builder
    assert Outcome("Even", odds.EVEN) in builder.temp_bins.get(18)
    assert Outcome("Even", odds.EVEN) in builder.temp_bins.get(36)


def test_odd_bets(built_builder):
    builder = built_builder
    assert Outcome("Odd", odds.EVEN) in builder.temp_bins.get(1)
    assert Outcome("Odd", odds.EVEN) in builder.temp_bins.get(17)


def test_five_bets(built_builder):
    builder = built_builder
    assert Outcome("Five", odds.FIVE) in builder.temp_bins.get(1)
    assert Outcome("Five", odds.FIVE) in builder.temp_bins.get(0)
    assert Outcome("Five", odds.FIVE) in builder.temp_bins.get(37)
