import random
from dataclasses import dataclass
from fractions import Fraction

import pytest

import casino.main
import casino.players


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
    wheel = casino.main.Wheel(rng)
    return wheel


@pytest.fixture
def seeded_dice():
    rng = random.Random()
    rng.seed(99998)
    dice = casino.main.Dice(rng)
    return dice


@pytest.fixture
def wheel_with_outcomes(mock_outcomes):
    wheel = casino.main.Wheel()
    wheel.add_outcomes(8, mock_outcomes)
    return wheel


@pytest.fixture(scope="module")
def patched_builder(monkey_module):
    monkey_module.setattr(casino.main, "Outcome", MockOutcome)
    monkey_module.setattr(casino.main, "Wheel", MockWheel)
    builder = casino.main.BinBuilder()
    builder.build_bins(casino.main.Wheel())

    return builder


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
def built_dice(monkey_module):
    builder = casino.main.ThrowBuilder()
    dice = casino.main.Dice()
    builder.build_throws(dice)
    return dice


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

    @property
    def event_id(self):
        return self.d1 + self.d2


@pytest.fixture
def mock_throw():
    return MockThrow


@pytest.fixture
def mock_throws():
    return [
        MockThrow(2, 6, MockOutcome("foo", 1), MockOutcome("bar", 2)),
        MockThrow(5, 5, MockOutcome("bar", 2), MockOutcome("har", 3)),
        MockThrow(1, 3, MockOutcome("foo", 1), MockOutcome("har", 3)),
    ]


@pytest.fixture
def sample_hard_one_outcomes():
    return {
        "one_roll": {
            "winners": {
                MockOutcome("one_roll_win_1", 1),
                MockOutcome("one_roll_win_2", 2),
                MockOutcome("one_roll_win_3", 3),
            },
            "losers": {
                MockOutcome("one_roll_lose_1", 4),
                MockOutcome("one_roll_lose_2", 5),
                MockOutcome("one_roll_lose_3", 6),
            },
        },
        "hardways": {
            "winners": {
                MockOutcome("hardways_win_1", 7),
                MockOutcome("hardways_win_2", 8),
                MockOutcome("hardways_win_3", 9),
            },
            "losers": {
                MockOutcome("hardways_lose_1", 10),
                MockOutcome("hardways_lose_2", 11),
                MockOutcome("hardways_lose_3", 12),
            },
        },
    }


@dataclass
class MockBet:
    amount: int
    outcome: casino.main.Outcome
    player: casino.players.Player

    def win_amount(self):
        return self.amount * 2

    def price(self):
        return self.amount

    def set_outcome(self, outcome):
        self.outcome = outcome

    def __str__(self) -> str:
        return f"{self.amount} on {self.outcome}"

    def __repr__(self) -> str:
        return f"Bet(amount={repr(self.amount)}, Outcome={repr(self.outcome)})"


@pytest.fixture
def mock_bet():
    return MockBet


@pytest.fixture
def sample_bets():
    return [
        MockBet(1, MockOutcome("Red", 1), MockPlayer()),  # type: ignore
        MockBet(2, MockOutcome("4-1 Split", 4), MockPlayer()),  # type: ignore
        MockBet(5, MockOutcome("Dozen 1", 6), MockPlayer()),  # type: ignore
    ]


@pytest.fixture
def invalid_bets():
    return [
        MockBet(0, MockOutcome("Red", 1), MockPlayer()),  # type: ignore
        MockBet(-1, MockOutcome("4-1 Split", 4), MockPlayer()),  # type: ignore
        MockBet(100, MockOutcome("Column 1", 6), MockPlayer()),  # type: ignore
    ]


@pytest.fixture
def craps_bet() -> MockBet:
    def _craps_bet(name):
        return MockBet(10, MockOutcome(name, 1), MockPlayer())  # type: ignore

    return _craps_bet  # type: ignore


class MockTable:
    def __init__(self, *bets):
        self.limit = 30
        self.bets = []
        self.game = None

    def set_game(self, game):
        self.game = game

    def place_bet(self, bet):
        self.bets.append(bet)
        bet.player.stake -= bet.price()

    def remove_bet(self, bet):
        self.bets.remove(bet)

    def contains_outcome(self, outcome_name):
        for bet in self.bets:
            if bet.outcome.name == outcome_name:
                return True

        return False

    def __iter__(self):
        return iter(self.bets[:])


@pytest.fixture
def mock_table():
    return MockTable


class MockPlayer:
    def __init__(self):
        self.outcome = MockOutcome("Black", 1)
        self.stake = 100

    def win(self, bet):
        self.stake += bet.win_amount()

    def lose(self, bet):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}()"


@pytest.fixture
def mock_player():
    return MockPlayer


@pytest.fixture
def override_player_abstract_methods():
    player_abs_methods = casino.players.Player.__abstractmethods__
    casino.players.Player.__abstractmethods__ = set()
    yield
    casino.players.Player.__abstractmethods__ = player_abs_methods


class MockGame:
    def __init__(self):
        self.table = MockTable()
        self.event_factory = MockWheel()

    def is_allowed(self):
        return True


@pytest.fixture
def mock_game():
    return MockGame


class MockCrapsGame:
    def __init__(self, dice, table):
        self.current_point = None
        self.table = table

    def craps(self, throw):
        ...

    def natural(self, throw) -> None:
        if self.current_point:
            self.current_point = None

    def eleven(self, throw):
        ...

    def point(self, throw):
        if self.current_point is None:
            self.current_point = "dice roll"  # Set point to value of dice roll.
        elif self.current_point == "dice roll":
            # Win this game and set point off.
            self.current_point = None

    def point_odds(self):
        return 1

    def __str__(self) -> str:
        return str(self.current_point) if self.current_point else "Point Off"


@pytest.fixture
def mock_craps_game(monkeypatch):
    return MockCrapsGame


@pytest.fixture
def override_craps_game_state_abs_methods():
    craps_game_state_abs_methods = casino.main.CrapsGameState.__abstractmethods__
    casino.main.CrapsGameState.__abstractmethods__ = set()
    yield
    casino.main.CrapsGameState.__abstractmethods__ = craps_game_state_abs_methods


class MockRandomEvent:
    def __init__(self, event_id):
        self.event_id = event_id


@pytest.fixture
def mock_random_events():
    return [
        MockRandomEvent(2),
        MockRandomEvent(3),
    ]


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
