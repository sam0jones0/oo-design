"""TODO"""

import pytest
import random

import roulette
from roulette.roulette import BinBuilder, Wheel


# Hack for broader scope monkeypatch:
@pytest.fixture(scope="module")
def monkey_module(request):
    from _pytest.monkeypatch import MonkeyPatch

    m_patch = MonkeyPatch()
    yield m_patch
    m_patch.undo()


@pytest.fixture(scope="module")
def patched_wheel(monkey_module):
    monkey_module.setattr(roulette.roulette, "Wheel", MockWheel)


class MockWheel:
    """Mock of `Wheel` class."""

    @staticmethod
    def add_outcomes(*args, **kwargs):
        return None

    def get_outcome(self, name):
        return MockOutcome("Black", 1)

    def choose(self):
        return tuple("bin_1")


@pytest.fixture(scope="module")
def mock_wheel():
    """Wheel.add_outcomes() mocked to not add outcomes to bins."""
    return MockWheel


@pytest.fixture
def seeded_wheel():
    rng = random.Random()
    # First randint(0, 37) with seed of 1 will return 8.
    rng.seed(1)
    wheel = Wheel()
    wheel.rng = rng
    return wheel


@pytest.fixture
def wheel_with_outcomes(mock_outcomes):
    wheel = Wheel()
    wheel.add_outcomes(8, mock_outcomes)
    return wheel


@pytest.fixture(scope="module")
def patched_builder(monkey_module):
    monkey_module.setattr(roulette.roulette, "Outcome", MockOutcome)
    monkey_module.setattr(roulette.roulette, "Wheel", MockWheel)
    wheel = Wheel()

    return wheel.bin_builder


class MockBuilder:
    def build_bins(self, *args):
        pass


@pytest.fixture(scope="module")
def do_not_build_bins(monkey_module):
    monkey_module.setattr(roulette.roulette, "BinBuilder", MockBuilder)


class MockOutcome:
    def __init__(self, name, odds):
        self.name = name
        self.odds = odds

    def __hash__(self):
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name} {self.odds}:1"

    def __repr__(self) -> str:
        return f"Outcome(name={repr(self.name)}, odds={repr(self.odds)})"


@pytest.fixture
def mock_outcomes():
    return [
        MockOutcome("foo", 1),
        MockOutcome("bar", 2),
        MockOutcome("har", 3),
    ]


class MockBet:
    def __init__(self, amount, outcome):
        self.amount = amount
        self.outcome = outcome

    def __str__(self) -> str:
        return f"{self.amount} on {self.outcome}"

    def __repr__(self) -> str:
        return f"Bet(amount={repr(self.amount)}, outcome={repr(self.outcome)})"

    def win_amount(self):
        return self.amount * 2


@pytest.fixture
def mock_bet():
    return MockBet


@pytest.fixture
def sample_bets():
    return [
        MockBet(10, MockOutcome("Red", 1)),
        MockBet(20, MockOutcome("4-1 Split", 4)),
        MockBet(50, MockOutcome("Dozen 1", 6)),
    ]


@pytest.fixture
def invalid_bets():
    return [
        MockBet(1, MockOutcome("Red", 1)),
        MockBet(-1, MockOutcome("4-1 Split", 4)),
        MockBet(1000, MockOutcome("Column 1", 6)),
    ]


class MockTable:
    def __init__(self):
        self.minimum = 10
        self.limit = 300
        self.wheel = MockWheel()

    def place_bet(self, *args):
        return "placed bet"


@pytest.fixture
def mock_table():
    return MockTable
