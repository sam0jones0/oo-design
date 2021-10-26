import pytest

import casino.main


class TestTable:
    @pytest.fixture(autouse=True)
    def _setup(self, mock_game):
        self.game = mock_game

    def test_empty_init(self):
        t = casino.main.Table()
        t.set_game(self.game)
        assert t.bets == []

    def test_multi_init(self, sample_bets):
        b1, b2, _ = sample_bets
        t = casino.main.Table()
        t.set_game(self.game)
        t.place_bet(b1)
        t.place_bet(b2)
        assert len(t.bets) == 2
        assert b1 in t.bets
        assert b2 in t.bets

    def test_place_bet(self, sample_bets):
        b1, b2, b3 = sample_bets
        t = casino.main.Table()
        t.set_game(self.game)
        for bet in sample_bets:
            t.place_bet(bet)
        assert len(t.bets) == 3
        assert b1 in t.bets
        assert b2 in t.bets

    def test_bets_total(self, sample_bets):
        b1, b2, b3 = sample_bets
        t = casino.main.Table()
        t.set_game(self.game)
        for bet in sample_bets:
            t.place_bet(bet)
        assert t.bets_total == 8
        t.clear()
        assert t.bets_total == 0
        assert t.bets == []

    def test_place_invalid_bet(self, invalid_bets):
        t = casino.main.Table()
        t.set_game(self.game)
        for bet in invalid_bets:
            with pytest.raises(casino.main.InvalidBet):
                t.place_bet(bet)

    def test_is_valid(self, sample_bets):
        t = casino.main.Table()
        t.set_game(self.game)
        for bet in sample_bets:
            t.place_bet(bet)
        # sum(bets.amount for bet in t) = 8
        assert t.validate()

    def test_iter(self, sample_bets):
        t = casino.main.Table()
        t.set_game(self.game)
        for bet in sample_bets:
            t.place_bet(bet)
        t_iter = iter(t)
        assert isinstance(next(t_iter), type(sample_bets[0]))

    def test_str_repr(self, sample_bets):
        t = casino.main.Table()
        t.set_game(self.game)
        for bet in sample_bets:
            t.place_bet(bet)
        assert str(t) == "1 on Red 1:1, 2 on 4-1 Split 4:1, 5 on Dozen 1 6:1"
        assert (
            repr(t)
            == "Table(Bet(amount=1, Outcome=Outcome(name='Red', odds=Fraction(1, 1))), "
            "Bet(amount=2, Outcome=Outcome(name='4-1 Split', odds=Fraction(4, 1))), "
            "Bet(amount=5, Outcome=Outcome(name='Dozen 1', odds=Fraction(6, 1))))"
        )
