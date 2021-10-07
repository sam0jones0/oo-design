"""TODO"""

import pytest

import casino.main


class TestThrows:
    """perform unit tests on the various classes of the `Throw` class hierarchy."""

    @pytest.fixture(autouse=True)
    def _game(self, mock_craps_game, mock_player, mock_table):
        """Use new `MockCrapsGame` instance for each test."""
        self._game = mock_craps_game("dice", mock_table())  # type: ignore

    def test_throw(self, sample_hard_one_outcomes, mock_bet, mock_outcome, mock_player):
        """Test the `Throw` superclass."""
        player = mock_player()
        throw = casino.main.Throw(1, 6, ["outcome_1"])  # type: ignore
        throw.add(["outcome_2"])  # type: ignore
        assert throw.d1 == 1
        assert throw.d2 == 6
        assert throw.key == (1, 6)
        assert throw.event_id == 7
        assert isinstance(throw.outcomes, frozenset)
        assert "outcome_1" in throw.outcomes
        assert "outcome_2" in throw.outcomes
        assert set(throw.outcomes) == throw.winners

        assert not throw.is_hard()
        throw.d1 = 6
        assert throw.is_hard()
        assert str(throw) == "6, 6"

        one_roll_winners = sample_hard_one_outcomes["one_roll"]["winners"]
        one_roll_losers = sample_hard_one_outcomes["one_roll"]["losers"]
        hardways_winners = sample_hard_one_outcomes["hardways"]["winners"]
        hardways_losers = sample_hard_one_outcomes["hardways"]["losers"]
        throw.add_one_roll(one_roll_winners, one_roll_losers)
        throw.add_hardways(hardways_winners, hardways_losers)

        assert throw.win_one_roll == one_roll_winners
        assert throw.lose_one_roll == one_roll_losers
        assert throw.win_hardway == hardways_winners
        assert throw.lose_hardway == hardways_losers
        assert throw.losers == one_roll_losers | hardways_losers
        assert len(throw.winners) == 8

        for outcome in one_roll_winners | one_roll_losers:
            assert throw.resolve_one_roll(mock_bet(10, outcome, player))
        for outcome in hardways_winners | hardways_losers:
            assert throw.resolve_hard_ways(mock_bet(10, outcome, player))

        a_bet = mock_bet(10, mock_outcome("some outcome", 1), player)
        assert not throw.resolve_one_roll(a_bet)
        assert not throw.resolve_hard_ways(a_bet)

        with pytest.raises(NotImplementedError):
            throw.update_game(self._game)

    def test_natural_throw(self):
        """Test `Throw` subclass `NaturalThrow`."""
        for d1, d2 in zip([4, 1, 1, 6, 5], [4, 1, 2, 6, 5]):
            with pytest.raises(ValueError):
                _ = casino.main.NaturalThrow(d1, d2, "outcome")  # type: ignore

        nat_throw = casino.main.NaturalThrow(1, 6, ["outcome_1"])  # type: ignore
        nat_throw.add(["outcome_2"])  # type: ignore
        assert nat_throw.d1 == 1
        assert nat_throw.d2 == 6
        assert nat_throw.key == (1, 6)
        assert nat_throw.event_id == 7
        assert isinstance(nat_throw.outcomes, frozenset)
        assert "outcome_1" in nat_throw.outcomes
        assert "outcome_2" in nat_throw.outcomes

        assert not nat_throw.is_hard()
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
                _ = casino.main.CrapsThrow(d1, d2, "outcome")  # type: ignore

        craps_throw = casino.main.CrapsThrow(1, 1, ["outcome_1"])  # type: ignore
        craps_throw.add(["outcome_2"])  # type: ignore
        assert craps_throw.d1 == 1
        assert craps_throw.d2 == 1
        assert craps_throw.key == (1, 1)
        assert craps_throw.event_id == 2
        assert isinstance(craps_throw.outcomes, frozenset)
        assert "outcome_1" in craps_throw.outcomes
        assert "outcome_2" in craps_throw.outcomes

        assert not craps_throw.is_hard()
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
                _ = casino.main.ElevenThrow(d1, d2, "outcome")  # type: ignore

        eleven_throw = casino.main.ElevenThrow(5, 6, ["outcome_1"])  # type: ignore
        eleven_throw.add(["outcome_2"])  # type: ignore
        assert eleven_throw.d1 == 5
        assert eleven_throw.d2 == 6
        assert eleven_throw.key == (5, 6)
        assert eleven_throw.event_id == 11
        assert isinstance(eleven_throw.outcomes, frozenset)
        assert "outcome_1" in eleven_throw.outcomes
        assert "outcome_2" in eleven_throw.outcomes

        assert not eleven_throw.is_hard()
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
                _ = casino.main.PointThrow(d1, d2, "outcome")  # type: ignore

        point_throw = casino.main.PointThrow(4, 4, ["outcome_1"])  # type: ignore
        point_throw.add(["outcome_2"])  # type: ignore
        assert point_throw.d1 == 4
        assert point_throw.d2 == 4
        assert point_throw.key == (4, 4)
        assert point_throw.event_id == 8
        assert isinstance(point_throw.outcomes, frozenset)
        assert "outcome_1" in point_throw.outcomes
        assert "outcome_2" in point_throw.outcomes

        assert point_throw.is_hard()
        point_throw.d1, point_throw.d2 = 3, 5
        assert not point_throw.is_hard()
        assert str(point_throw) == "3, 5"

        point_throw.update_game(self._game)
        assert self._game.current_point == "dice roll"
        point_throw.update_game(self._game)
        assert self._game.current_point is None
