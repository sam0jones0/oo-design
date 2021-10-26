from fractions import Fraction

import pytest

import casino.main
import tests.conftest


class TestCrapsGamePointOn:
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
        self.state = casino.main.CrapsGamePointOn(point=6, game=self.game)

        assert self.table == self.game.table
        assert self.game == self.table.game

    def test_is_valid(self, craps_bet):
        buy_five_bet = craps_bet("Buy 5")
        buy_six_bet = craps_bet("Buy 6")
        lay_five_bet = craps_bet("Lay 5")
        lay_six_bet = craps_bet("Lay 6")
        pass_bet = craps_bet("Pass Line")
        come_bet = craps_bet("Come Line")
        prop_two_bet = craps_bet("Proposition 2")
        field_bet = craps_bet("Field")
        assert self.state.is_valid(buy_five_bet.outcome)
        assert not self.state.is_valid(buy_six_bet.outcome)
        assert self.state.is_valid(lay_five_bet.outcome)
        assert not self.state.is_valid(lay_six_bet.outcome)
        assert not self.state.is_valid(pass_bet.outcome)
        assert self.state.is_valid(come_bet.outcome)
        assert self.state.is_valid(prop_two_bet.outcome)
        assert self.state.is_valid(field_bet.outcome)

    def test_is_working(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        come_bet = craps_bet("Come Line")
        prop_two_bet = craps_bet("Proposition 2")
        assert self.state.is_working(pass_bet.outcome)
        assert self.state.is_working(come_bet.outcome)
        assert self.state.is_working(prop_two_bet.outcome)

    def test_craps_throw(self, craps_bet):
        dont_come_bet = craps_bet("Don't Come Line")
        come_bet = craps_bet("Come Line")
        come_odds_bet = craps_bet("Come Point 6 Odds")
        pass_bet = craps_bet("Pass Line")
        dont_pass_bet = craps_bet("Don't Pass Line")
        self.table.place_bet(dont_come_bet)
        self.table.place_bet(come_bet)
        self.table.place_bet(come_odds_bet)
        self.table.place_bet(pass_bet)
        self.table.place_bet(dont_pass_bet)

        craps_throw = casino.main.CrapsThrow(1, 2)
        self.state = self.state.craps(craps_throw)

        assert dont_come_bet.player.stake == 110
        assert come_bet.player.stake == 90
        assert come_odds_bet.player.stake == 90
        assert pass_bet.player.stake == 90
        assert dont_pass_bet.player.stake == 90

        assert len(self.table.bets) == 3
        assert isinstance(self.state, casino.main.CrapsGamePointOn)

    def test_natural_throw(self, craps_bet):
        dont_pass_bet = craps_bet("Don't Pass Line")
        dont_pass_odds = craps_bet("Don't Pass Odds")
        dont_come_point_bet = craps_bet("Don't Come Point 5")
        dont_come_point_odds_bet = craps_bet("Don't Come Point 9 Odds")
        pass_bet = craps_bet("Pass Line")
        dont_come_line_bet = craps_bet("Don't Come Line")
        come_point_bet = craps_bet("Come Point 4")
        come_point_odds_bet = craps_bet("Come Point 10 Odds")
        self.table.place_bet(dont_pass_bet)
        self.table.place_bet(dont_pass_odds)
        self.table.place_bet(dont_come_point_bet)
        self.table.place_bet(dont_come_point_odds_bet)
        self.table.place_bet(pass_bet)
        self.table.place_bet(dont_come_line_bet)
        self.table.place_bet(come_point_bet)
        self.table.place_bet(come_point_odds_bet)

        natural_throw = casino.main.NaturalThrow(3, 4)
        self.state = self.state.natural(natural_throw)

        assert dont_pass_bet.player.stake == 110
        assert dont_pass_odds.player.stake == 110
        assert dont_come_point_bet.player.stake == 110
        assert dont_come_point_odds_bet.player.stake == 110
        assert pass_bet.player.stake == 90
        assert dont_come_line_bet.player.stake == 90
        assert come_point_bet.player.stake == 90
        assert come_point_odds_bet.player.stake == 90

        assert isinstance(self.state, casino.main.CrapsGamePointOff)
        assert len(self.table.bets) == 0

    def test_eleven_throw(self, craps_bet):
        dont_come_bet = craps_bet("Don't Come Line")
        come_bet = craps_bet("Come Line")
        come_odds_bet = craps_bet("Come Point 6 Odds")
        pass_bet = craps_bet("Pass Line")
        dont_pass_bet = craps_bet("Don't Pass Line")
        self.table.place_bet(dont_come_bet)
        self.table.place_bet(come_bet)
        self.table.place_bet(come_odds_bet)
        self.table.place_bet(pass_bet)
        self.table.place_bet(dont_pass_bet)

        eleven_throw = casino.main.ElevenThrow(6, 5)
        self.state = self.state.eleven(eleven_throw)

        assert dont_come_bet.player.stake == 90
        assert come_bet.player.stake == 110
        assert come_odds_bet.player.stake == 90
        assert pass_bet.player.stake == 90
        assert dont_pass_bet.player.stake == 90

        assert len(self.table.bets) == 3
        assert isinstance(self.state, casino.main.CrapsGamePointOn)

    def test_point_throw_point_made(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        pass_odds_bet = craps_bet("Pass Odds")
        dont_pass_bet = craps_bet("Don't Pass Line")
        dont_pass_odds_bet = craps_bet("Don't Pass Odds")
        self.table.place_bet(pass_bet)
        self.table.place_bet(pass_odds_bet)
        self.table.place_bet(dont_pass_bet)
        self.table.place_bet(dont_pass_odds_bet)
        assert len(self.table.bets) == 4

        point_throw = casino.main.PointThrow(2, 4)  # Point is 6.
        self.state = self.state.point(point_throw)

        assert pass_bet.player.stake == 110
        assert pass_odds_bet.player.stake == 110
        assert dont_pass_bet.player.stake == 90
        assert dont_pass_odds_bet.player.stake == 90

        assert len(self.table.bets) == 0
        assert isinstance(self.state, casino.main.CrapsGamePointOff)

    def test_point_throw_point_not_made(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        come_point_bet = craps_bet("Come Point 5")
        come_point_odds_bet = craps_bet("Come Point 5 Odds")
        dont_come_point_bet = craps_bet("Don't Come Point 5")
        dont_come_point_odds_bet = craps_bet("Don't Come Point 5 Odds")
        other_come_point_bet = craps_bet("Come Point 8")
        self.table.place_bet(pass_bet)
        self.table.place_bet(come_point_bet)
        self.table.place_bet(come_point_odds_bet)
        self.table.place_bet(dont_come_point_bet)
        self.table.place_bet(dont_come_point_odds_bet)
        self.table.place_bet(other_come_point_bet)

        point_throw = casino.main.PointThrow(1, 4)  # Point is 6.
        self.state = self.state.point(point_throw)

        assert pass_bet.player.stake == 90
        assert come_point_bet.player.stake == 110
        assert come_point_odds_bet.player.stake == 110
        assert dont_come_point_bet.player.stake == 90
        assert dont_come_point_odds_bet.player.stake == 90
        assert other_come_point_bet.player.stake == 90

        assert len(self.table.bets) == 2
        assert isinstance(self.state, casino.main.CrapsGamePointOn)

    def test_point_throw_come_line_move_to_throw(self, craps_bet):
        pass_bet = craps_bet("Pass Line")
        come_line_bet = craps_bet("Come Line")
        dont_come_line_bet = craps_bet("Don't Come Line")
        self.table.place_bet(pass_bet)
        self.table.place_bet(come_line_bet)
        self.table.place_bet(dont_come_line_bet)

        point_throw = casino.main.PointThrow(4, 4)
        self.state = self.state.point(point_throw)

        assert come_line_bet.outcome.name == "Come Point 8"
        assert dont_come_line_bet.outcome.name == "Don't Come Point 8"

        assert len(self.table.bets) == 3
        assert isinstance(self.state, casino.main.CrapsGamePointOn)

    def test_point_outcome_odds(self):
        assert self.state.point_outcome_odds() == Fraction(6, 5)

    def test_str(self):
        assert self.state.__str__() == "The Point Is 6"
