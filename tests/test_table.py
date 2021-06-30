"""
TODO
"""

import pytest

from roulette.roulette import Bet, Table, InvalidBet

# TODO: Test bets_total counter.


def test_empty_init():
    t = Table()
    assert t.bets == []


def test_multi_init(sample_bets):
    b1, b2, _ = sample_bets
    t = Table(b1, b2)
    assert len(t.bets) == 2
    assert b1 in t.bets
    assert b2 in t.bets


def test_place_bet(sample_bets):
    b1, b2, b3 = sample_bets
    t = Table(b3)
    t.place_bet(b1)
    t.place_bet(b2)
    assert len(t.bets) == 3
    assert b1 in t.bets
    assert b2 in t.bets


def test_place_invalid_bet(invalid_bets):
    t = Table()
    for bet in invalid_bets:
        with pytest.raises(InvalidBet):
            t.place_bet(bet)


def test_is_valid(sample_bets):
    t = Table(*sample_bets)
    # sum(bets.amount for bet in t) = 80
    assert t.is_valid()


def test_iter(sample_bets):
    t = Table(*sample_bets)
    t_iter = iter(t)
    assert isinstance(next(t_iter), Bet)


def test_str_repr(sample_bets):
    t = Table(*sample_bets)
    assert str(t) == "10 on Red 1:1, 20 on 4-1 Split 4:1, 50 on Dozen 1 6:1"
    assert (
        repr(t) == "Table(Bet(amount=10, outcome=Outcome(name='Red', odds=1)), "
        "Bet(amount=20, outcome=Outcome(name='4-1 Split', odds=4)), "
        "Bet(amount=50, outcome=Outcome(name='Dozen 1', odds=6)))"
    )
