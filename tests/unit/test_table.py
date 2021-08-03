"""
TODO
"""

import pytest

from casino.main import Table, InvalidBet


@pytest.mark.usefixtures("patched_wheel")
class TestTable:
    def test_patched_wheel(self):
        t = Table()
        assert t.wheel.choose() == tuple("bin_1")

    def test_empty_init(self):
        t = Table()
        assert t.bets == []

    def test_multi_init(self, sample_bets):
        b1, b2, _ = sample_bets
        t = Table(b1, b2)
        assert len(t.bets) == 2
        assert b1 in t.bets
        assert b2 in t.bets

    def test_place_bet(self, sample_bets):
        b1, b2, b3 = sample_bets
        t = Table(b3)
        t.place_bet(b1)
        t.place_bet(b2)
        assert len(t.bets) == 3
        assert b1 in t.bets
        assert b2 in t.bets

    def test_bets_total(self, sample_bets):
        b1, b2, b3 = sample_bets
        t = Table(b1, b2)
        t.place_bet(b3)
        assert t.bets_total == 8
        t.clear()
        assert t.bets_total == 0
        assert t.bets == []

    def test_place_invalid_bet(self, invalid_bets):
        t = Table()
        for bet in invalid_bets:
            with pytest.raises(InvalidBet):
                t.place_bet(bet)

    def test_is_valid(self, sample_bets):
        t = Table(*sample_bets)
        # sum(bets.amount for bet in t) = 8
        assert t.validate()

    def test_iter(self, sample_bets):
        t = Table(*sample_bets)
        t_iter = iter(t)
        assert isinstance(next(t_iter), type(sample_bets[0]))

    def test_str_repr(self, sample_bets):
        t = Table(*sample_bets)
        assert str(t) == "1 on Red 1:1, 2 on 4-1 Split 4:1, 5 on Dozen 1 6:1"
        assert (
            repr(t) == "Table(Bet(amount=1, outcome=Outcome(name='Red', odds=1)), "
            "Bet(amount=2, outcome=Outcome(name='4-1 Split', odds=4)), "
            "Bet(amount=5, outcome=Outcome(name='Dozen 1', odds=6)))"
        )
