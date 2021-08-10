"""TODO"""

import pytest

import casino
from casino.main import Throw, CrapsThrow, PointThrow, ElevenThrow, NaturalThrow


class TestThrows:
    """perform unit tests on the various classes of the `Throw` class hierarchy."""

    @pytest.fixture(autouse=True)
    def _game(self, mock_craps_game):
        """Use new `MockCrapsGame` instance for each test."""
        self._game = casino.main.CrapsGame()

    def test_throw(self):
        """Test the `Throw` superclass."""
        throw = Throw(1, 6, ["outcome_1"])  # type: ignore
        throw.add(["outcome_2"])  # type: ignore
        assert throw.d1 == 1
        assert throw.d2 == 6
        assert throw.key == (1, 6)
        assert isinstance(throw.outcomes, frozenset)
        assert "outcome_1" in throw.outcomes
        assert "outcome_2" in throw.outcomes

        assert not throw.hard()
        throw.d1 = 6
        assert throw.hard()
        assert str(throw) == "6, 6"

        with pytest.raises(NotImplementedError):
            throw.update_game(self._game)

    def test_natural_throw(self):
        """Test `Throw` subclass `NaturalThrow`."""
        for d1, d2 in zip([4, 1, 1, 6, 5], [4, 1, 2, 6, 5]):
            with pytest.raises(ValueError):
                _ = NaturalThrow(d1, d2, "outcome")  # type: ignore

        nat_throw = NaturalThrow(1, 6, ["outcome_1"])  # type: ignore
        nat_throw.add(["outcome_2"])  # type: ignore  # type: ignore
        assert nat_throw.d1 == 1
        assert nat_throw.d2 == 6
        assert nat_throw.key == (1, 6)
        assert isinstance(nat_throw.outcomes, frozenset)
        assert "outcome_1" in nat_throw.outcomes
        assert "outcome_2" in nat_throw.outcomes

        assert not nat_throw.hard()
        assert str(nat_throw) == "1, 6"

        nat_throw.update_game(self._game)
        assert self._game.current_point is None
        self._game.current_point = 4
        nat_throw.update_game(self._game)
        assert self._game.current_point is None

    def test_craps_throw(self):
        """Test `Throw` subclass `CrapsThrow`."""
        for d1, d2 in zip([2, 2, 3, 5, 5], [2, 3, 3, 5, 6]):
            with pytest.raises(ValueError):
                _ = CrapsThrow(d1, d2, "outcome")  # type: ignore

        craps_throw = CrapsThrow(1, 1, ["outcome_1"])  # type: ignore
        craps_throw.add(["outcome_2"])  # type: ignore
        assert craps_throw.d1 == 1
        assert craps_throw.d2 == 1
        assert craps_throw.key == (1, 1)
        assert isinstance(craps_throw.outcomes, frozenset)
        assert "outcome_1" in craps_throw.outcomes
        assert "outcome_2" in craps_throw.outcomes

        assert not craps_throw.hard()
        assert str(craps_throw) == "1, 1"

        assert self._game.current_point is None
        craps_throw.update_game(self._game)
        assert self._game.current_point is None
        self._game.current_point = 5
        craps_throw.update_game(self._game)
        assert self._game.current_point == 5

    def test_eleven_throw(self):
        """Test `Throw` subclass `ElevenThrow`."""
        for d1, d2 in zip([4, 1, 1, 6, 5], [3, 1, 2, 6, 5]):
            with pytest.raises(ValueError):
                _ = ElevenThrow(d1, d2, "outcome")  # type: ignore

        eleven_throw = ElevenThrow(5, 6, ["outcome_1"])  # type: ignore
        eleven_throw.add(["outcome_2"])  # type: ignore
        assert eleven_throw.d1 == 5
        assert eleven_throw.d2 == 6
        assert eleven_throw.key == (5, 6)
        assert isinstance(eleven_throw.outcomes, frozenset)
        assert "outcome_1" in eleven_throw.outcomes
        assert "outcome_2" in eleven_throw.outcomes

        assert not eleven_throw.hard()
        assert str(eleven_throw) == "5, 6"

        assert self._game.current_point is None
        eleven_throw.update_game(self._game)
        assert self._game.current_point is None
        self._game.current_point = 5
        eleven_throw.update_game(self._game)
        assert self._game.current_point == 5

    def test_point_throw(self):
        """Test `Throw` subclass `PointThrow`."""
        for d1, d2 in zip([4, 1, 1, 6, 6], [3, 1, 2, 5, 6]):
            with pytest.raises(ValueError):
                _ = PointThrow(d1, d2, "outcome")  # type: ignore

        point_throw = PointThrow(4, 4, ["outcome_1"])  # type: ignore
        point_throw.add(["outcome_2"])  # type: ignore
        assert point_throw.d1 == 4
        assert point_throw.d2 == 4
        assert point_throw.key == (4, 4)
        assert isinstance(point_throw.outcomes, frozenset)
        assert "outcome_1" in point_throw.outcomes
        assert "outcome_2" in point_throw.outcomes

        assert point_throw.hard()
        point_throw.d1, point_throw.d2 = 3, 5
        assert not point_throw.hard()
        assert str(point_throw) == "3, 5"

        point_throw.update_game(self._game)
        assert self._game.current_point == "dice roll"
        point_throw.update_game(self._game)
        assert self._game.current_point is None
