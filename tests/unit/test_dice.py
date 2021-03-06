import random

import pytest

import casino.main


@pytest.mark.usefixtures("do_not_build_throws")
class TestDice:
    @pytest.fixture(autouse=True)
    def _mock_throws(self, mock_throws):
        self.mock_throws = mock_throws

    def test_add(self):
        dice = casino.main.Dice()
        for throw in self.mock_throws:
            dice.add_throw(throw)
        assert len(dice.throws) == len(self.mock_throws)
        for throw in self.mock_throws:
            assert throw in dice.throws.values()

    def test_roll_and_get(self):
        rng = random.Random()
        rng.seed(1)
        dice = casino.main.Dice()
        dice.rng = rng
        for throw in self.mock_throws:
            dice.add_throw(throw)

        assert dice.choose() == self.mock_throws[0]
        assert dice.choose() == self.mock_throws[2]
        assert dice.choose() == self.mock_throws[0]
        assert dice.choose() == self.mock_throws[1]

        assert dice.get_event((2, 6)) == self.mock_throws[0]
        assert dice.get_event((5, 5)) == self.mock_throws[1]
        assert dice.get_event((1, 3)) == self.mock_throws[2]
