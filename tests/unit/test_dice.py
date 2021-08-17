"""TODO"""

import random

import pytest

from casino.main import Dice


@pytest.mark.usefixtures("do_not_build_throws")
class TestDice:
    @pytest.fixture(autouse=True)
    def _mock_throws(self, mock_throws):
        self.mock_throws = mock_throws

    def test_add(self):
        dice = Dice()
        for throw in self.mock_throws:
            dice.add_throw(throw)
        assert len(dice.throws) == len(self.mock_throws)
        for throw in self.mock_throws:
            assert throw in dice.throws.values()

    def test_roll_and_get(self):
        rng = random.Random()
        rng.seed(1)
        dice = Dice()
        dice.rng = rng
        for throw in self.mock_throws:
            dice.add_throw(throw)

        assert dice.roll() == self.mock_throws[0]
        assert dice.roll() == self.mock_throws[2]
        assert dice.roll() == self.mock_throws[0]
        assert dice.roll() == self.mock_throws[1]

        assert dice._get_throw(2, 6) == self.mock_throws[0]
        assert dice._get_throw(5, 5) == self.mock_throws[1]
        assert dice._get_throw(1, 3) == self.mock_throws[2]
