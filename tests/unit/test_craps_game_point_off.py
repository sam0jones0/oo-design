import pytest

import casino.main


class TestCrapsGamePointOff:
    @pytest.fixture(autouse=True)
    def _setup(self, monkeypatch, mock_craps_game, mock_table, mock_throw):
        monkeypatch.setattr(casino.main, "CrapsGame", mock_craps_game)
        monkeypatch.setattr(casino.main, "Table", mock_table)
        monkeypatch.setattr(casino.main, "NaturalThrow", mock_throw)
        monkeypatch.setattr(casino.main, "ElevenThrow", mock_throw)
        monkeypatch.setattr(casino.main, "CrapsThrow", mock_throw)
        monkeypatch.setattr(casino.main, "PointThrow", mock_throw)

        self.table = casino.main.Table()
        self.game = casino.main.CrapsGame("dice", self.table)  # type: ignore
        self.table.set_game(self.game)
        self.state = casino.main.CrapsGamePointOff(self.game)

        assert self.table == self.game.table
        assert self.game == self.table.game

    def test_is_valid(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        come_bet = craps_bet("Come Line")

        assert self.state.is_valid(pass_bet.outcome)
        assert not self.state.is_valid(come_bet.outcome)

    def test_is_working(self, craps_bet):
        dont_come_odds_bet = craps_bet("Don't Come Point 6 Odds")
        come_odds_bet = craps_bet("Come Point 6 Odds")
        pass_bet = craps_bet("Pass Line")
        dont_pass_bet = craps_bet("Don't Pass Line")
        assert self.state.is_working(dont_come_odds_bet.outcome)
        assert not self.state.is_working(come_odds_bet.outcome)
        assert self.state.is_working(pass_bet.outcome)
        assert self.state.is_working(dont_pass_bet.outcome)

    def test_craps_throw(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        dont_pass_bet = craps_bet("Don't Pass Line")
        come_bet = craps_bet("Come Line")
        self.table.place_bet(pass_bet)
        self.table.place_bet(dont_pass_bet)
        self.table.place_bet(come_bet)

        twelve_throw = casino.main.CrapsThrow(6, 6)
        self.state = self.state.craps(twelve_throw)

        assert pass_bet.player.stake == 90
        assert dont_pass_bet.player.stake == 100
        assert come_bet.player.stake == 90
        assert len(self.table.bets) == 1

        self.table.place_bet(dont_pass_bet)
        three_throw = casino.main.CrapsThrow(1, 2)
        self.state = self.state.craps(three_throw)

        assert isinstance(self.state, casino.main.CrapsGamePointOff)
        assert dont_pass_bet.player.stake == 110

    def test_natural_throw(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        dont_pass_bet = craps_bet("Don't Pass Line")
        dont_come_bet = craps_bet("Don't Come Line")
        self.table.place_bet(pass_bet)
        self.table.place_bet(dont_pass_bet)
        self.table.place_bet(dont_come_bet)

        seven_throw = casino.main.NaturalThrow(2, 5)
        self.state = self.state.natural(seven_throw)

        assert pass_bet.player.stake == 110
        assert dont_pass_bet.player.stake == 90
        assert dont_come_bet.player.stake == 90

        assert len(self.table.bets) == 0
        assert isinstance(self.state, casino.main.CrapsGamePointOff)

    def test_eleven_throw(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        dont_pass_bet = craps_bet("Don't Pass Line")
        dont_come_bet = craps_bet("Don't Come Line")
        self.table.place_bet(pass_bet)
        self.table.place_bet(dont_pass_bet)
        self.table.place_bet(dont_come_bet)

        eleven_throw = casino.main.ElevenThrow(5, 6)
        self.state = self.state.eleven(eleven_throw)

        assert pass_bet.player.stake == 110
        assert dont_pass_bet.player.stake == 90
        assert dont_come_bet.player.stake == 90

        assert len(self.table.bets) == 1
        assert isinstance(self.state, casino.main.CrapsGamePointOff)

    def test_point_throw(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        come_point_bet = craps_bet("Come Point 6")
        dont_come_point_bet = craps_bet("Don't Come Point 5")
        come_odds_bet = craps_bet("Come Point 6 Odds")
        dont_come_odds_bet = craps_bet("Don't Come Point 5 Odds")
        self.table.place_bet(pass_bet)
        self.table.place_bet(come_point_bet)
        self.table.place_bet(dont_come_point_bet)
        self.table.place_bet(come_odds_bet)
        self.table.place_bet(dont_come_odds_bet)

        point_throw = casino.main.PointThrow(2, 4)
        # Come/Don't Come Point x [Odds] where x is 6 should be pushed.
        self.state = self.state.point(point_throw)

        assert pass_bet.player.stake == 90
        assert come_point_bet.player.stake == 100
        assert dont_come_point_bet.player.stake == 90
        assert come_odds_bet.player.stake == 100
        assert dont_come_odds_bet.player.stake == 90

        assert len(self.table.bets) == 3
        assert isinstance(self.state, casino.main.CrapsGamePointOn)

    def test_point_outcome_odds(self):
        assert self.state.point_outcome_odds() is None

    def test_str(self):
        assert self.state.__str__() == "The Point Is Off"
