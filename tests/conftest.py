"""TODO"""

import pytest
import random

from roulette.roulette import Bet, Outcome, BinBuilder, Wheel


class MockWheel:
    """Mock of `Wheel` class."""

    @staticmethod
    def add_outcomes(*args, **kwargs):
        return None


@pytest.fixture(scope="module")
def mock_wheel():
    """Wheel.add_outcomes() mocked to not add outcomes to bins."""
    return MockWheel


@pytest.fixture(scope="module")
def built_builder(mock_wheel):
    wheel = MockWheel()
    builder = BinBuilder()
    builder.build_bins(wheel)  # Type: ignore
    return builder


@pytest.fixture
def sample_bets():
    return [
        Bet(10, Outcome("Red", 1)),
        Bet(20, Outcome("4-1 Split", 4)),
        Bet(50, Outcome("Dozen 1", 6)),
    ]


@pytest.fixture
def invalid_bets():
    return [
        Bet(1, Outcome("Red", 1)),
        Bet(-1, Outcome("4-1 Split", 4)),
        Bet(1000, Outcome("Column 1", 6)),
    ]


@pytest.fixture
def seeded_wheel():
    rng = random.Random()
    # First randint(0, 37) with seed of 1 will return 8.
    rng.seed(1)
    wheel = Wheel(rng=rng)
    return wheel


@pytest.fixture
def wheel_with_outcomes(sample_outcomes):
    wheel = Wheel()
    wheel.add_outcomes(8, sample_outcomes)
    return wheel


@pytest.fixture
def sample_outcomes():
    return [
        Outcome("foo", 1),
        Outcome("bar", 2),
        Outcome("har", 3),
    ]
