"""TODO"""

import random
from fractions import Fraction

import pytest

import casino
from casino.main import BinBuilder, Wheel, ThrowBuilder, Dice


# Hack for broader scope monkeypatch:
@pytest.fixture(scope="module")
def monkey_module(request):
    from _pytest.monkeypatch import MonkeyPatch

    m_patch = MonkeyPatch()
    yield m_patch
    m_patch.undo()


@pytest.fixture(scope="module")
def patched_wheel(monkey_module):
    monkey_module.setattr(casino.main, "Wheel", MockWheel)


class MockWheel:
    """Mock of `Wheel` class."""

    def __init__(self):
        self.all_outcomes = {
            "Red": MockOutcome("Red", 1),
            "4-1 Split": MockOutcome("4-1 Split", 4),
            "Dozen 1": MockOutcome("Dozen 1", 6),
        }

    def add_outcomes(*args, **kwargs):
        return None

    def get_outcome(self, name):
        return MockOutcome("red", 1)

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
    monkey_module.setattr(casino.main, "Outcome", MockOutcome)
    monkey_module.setattr(casino.main, "Wheel", MockWheel)
    wheel = Wheel()

    return wheel.bin_builder


class MockBuilder:
    def build_bins(self, *args):
        pass


@pytest.fixture(scope="module")
def do_not_build_bins(monkey_module):
    monkey_module.setattr(casino.main, "BinBuilder", MockBuilder)


class MockThrowBuilder:
    def build_throws(self, *args):
        pass


@pytest.fixture(scope="module")
def do_not_build_throws(monkey_module):
    monkey_module.setattr(casino.main, "ThrowBuilder", MockThrowBuilder)


@pytest.fixture(scope="module")
def built_throws(monkey_module):
    builder = ThrowBuilder()
    dice = Dice()
    builder.build_throws(dice)
    return dice.throws


class MockOutcome:
    def __init__(self, name, odds):
        self.name = name
        if isinstance(odds, int):
            self.odds = Fraction(odds, 1)
        elif isinstance(odds, Fraction):
            self.odds = odds
        else:
            raise TypeError("outcome_odds must be either an int or Fraction.")

    def __hash__(self):
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name} {self.odds}:1"

    def __repr__(self) -> str:
        return f"Outcome(name={repr(self.name)}, odds={repr(self.odds)})"

    def __eq__(self, other):
        if not isinstance(other, MockOutcome):
            return NotImplemented
        return self.name == other.name


@pytest.fixture
def mock_outcome():
    return MockOutcome


@pytest.fixture
def mock_outcomes():
    return [
        MockOutcome("foo", 1),
        MockOutcome("bar", 2),
        MockOutcome("har", 3),
    ]


class MockThrow:
    def __init__(self, d1, d2, *outcomes):
        self.d1 = d1
        self.d2 = d2
        self.outcomes = frozenset(outcomes)
        self.key = (d1, d2)


@pytest.fixture
def mock_throws():
    return [
        MockThrow(2, 6, MockOutcome("foo", 1), MockOutcome("bar", 2)),
        MockThrow(5, 5, MockOutcome("bar", 2), MockOutcome("har", 3)),
        MockThrow(1, 3, MockOutcome("foo", 1), MockOutcome("har", 3)),
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
        MockBet(1, MockOutcome("Red", 1)),
        MockBet(2, MockOutcome("4-1 Split", 4)),
        MockBet(5, MockOutcome("Dozen 1", 6)),
    ]


@pytest.fixture
def invalid_bets():
    return [
        MockBet(0, MockOutcome("Red", 1)),
        MockBet(-1, MockOutcome("4-1 Split", 4)),
        MockBet(100, MockOutcome("Column 1", 6)),
    ]


class MockTable:
    def __init__(self):
        self.limit = 30
        self.wheel = MockWheel()
        self.bets = []

    def place_bet(self, bet):
        self.bets.append(bet)


@pytest.fixture
def mock_table():
    return MockTable


class MockPlayer:
    def __init__(self):
        self.outcome = MockOutcome("Black", 1)


@pytest.fixture
def mock_player():
    return MockPlayer


class MockGame:
    def __init__(self):
        self.table = MockTable()


@pytest.fixture
def mock_game():
    return MockGame


class MockSimulator:
    def __init__(self, *args, **kwargs):
        self.durations = MockIntegerStatistics()
        self.maxima = MockIntegerStatistics()
        self.end_stakes = MockIntegerStatistics()

    def gather(self):
        return


@pytest.fixture
def mock_simulator():
    return MockSimulator


class MockIntegerStatistics:
    def mean(self):
        return 10.1

    def stdev(self):
        return 1.1


class MockCrapsGame:
    def __init__(self):
        self.current_point = None

    def craps(self):
        ...

    def natural(self) -> None:
        if self.current_point:
            self.current_point = None

    def eleven(self):
        ...

    def point(self):
        if self.current_point is None:
            self.current_point = "dice roll"  # Set point to value of dice roll.
        elif self.current_point == "dice roll":
            # Win this game and set point off.
            self.current_point = None

    def __str__(self) -> str:
        return str(self.current_point) if self.current_point else "Point Off"


@pytest.fixture
def mock_craps_game(monkeypatch):
    monkeypatch.setattr(casino.main, "CrapsGame", MockCrapsGame)


class MockRandomEvent:
    def __init__(self, event_id):
        self.event_id = event_id


@pytest.fixture
def mock_random_events():
    return [
        MockRandomEvent(2),
        MockRandomEvent(3),
    ]
