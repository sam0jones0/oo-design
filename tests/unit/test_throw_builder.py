"""TODO"""

from collections import Counter

import pytest

from casino.main import (
    CrapsThrow,
    NaturalThrow,
    ElevenThrow,
    PointThrow,
    Outcome,
    OutcomeField,
    OutcomeHorn,
    Fraction,
)


@pytest.mark.usefixtures("built_throws")
class TestThrowBuilder:
    def test_correct_throw_object(self, built_throws):
        for k, v in built_throws.items():
            key_sum = sum(k)
            if key_sum in {2, 3, 12}:
                assert isinstance(v, CrapsThrow)
            elif key_sum == 7:
                assert isinstance(v, NaturalThrow)
            elif key_sum == 11:
                assert isinstance(v, ElevenThrow)
            else:
                assert isinstance(v, PointThrow)

    def test_correct_number_outcomes(self, built_throws):
        count = Counter(
            [
                outcome.name
                for sublist in list(built_throws.values())
                for outcome in sublist.outcomes
            ]
        )
        assert count["Field"] == 16
        assert count["Horn"] == 6
        assert count["Proposition 7"] == 6
        assert count["Craps"] == 4
        assert count["Easy 5"] == 4
        assert count["Easy 6"] == 4
        assert count["Easy 8"] == 4
        assert count["Easy 9"] == 4
        assert count["Proposition 3"] == 2
        assert count["Easy 4"] == 2
        assert count["Easy 10"] == 2
        assert count["Proposition 11"] == 2
        assert count["Proposition 2"] == 1
        assert count["Hard 4"] == 1
        assert count["Hard 6"] == 1
        assert count["Hard 8"] == 1
        assert count["Hard 10"] == 1
        assert count["Proposition 12"] == 1

    def test_random_sample_throws(self, built_throws):
        throw_1 = built_throws[(1, 1)]
        assert len(throw_1.outcomes) == 4
        assert Outcome(name="Proposition 2", outcome_odds=Fraction(30, 1)) in throw_1
        assert OutcomeHorn(name="Horn", outcome_odds=Fraction(3, 1)) in throw_1
        assert OutcomeField(name="Field", outcome_odds=Fraction(1, 1)) in throw_1
        assert Outcome(name="Craps", outcome_odds=Fraction(7, 1)) in throw_1

        throw_2 = built_throws[(1, 3)]
        assert len(throw_2.outcomes) == 2
        assert OutcomeField(name="Field", outcome_odds=Fraction(1, 1)) in throw_2
        assert Outcome(name="Easy 4", outcome_odds=Fraction(0, 1)) in throw_2

        throw_3 = built_throws[(3, 3)]
        assert len(throw_3.outcomes) == 1
        assert Outcome(name="Hard 6", outcome_odds=Fraction(9, 1)) in throw_3

        throw_4 = built_throws[(4, 3)]
        assert len(throw_4.outcomes) == 1
        assert Outcome(name="Proposition 7", outcome_odds=Fraction(4, 1)) in throw_4

        throw_5 = built_throws[(4, 6)]
        assert len(throw_5.outcomes) == 2
        assert OutcomeField(name="Field", outcome_odds=Fraction(1, 1)) in throw_5
        assert Outcome(name="Easy 10", outcome_odds=Fraction(0, 1)) in throw_5

        throw_6 = built_throws[(5, 6)]
        assert len(throw_6.outcomes) == 3
        assert OutcomeHorn(name="Horn", outcome_odds=Fraction(3, 1)) in throw_6
        assert OutcomeField(name="Field", outcome_odds=Fraction(1, 1)) in throw_6
        assert Outcome(name="Proposition 11", outcome_odds=Fraction(15, 1)) in throw_6

        throw_7 = built_throws[(6, 6)]
        assert len(throw_7.outcomes) == 4
        assert Outcome(name="Proposition 12", outcome_odds=Fraction(30, 1)) in throw_7
        assert OutcomeHorn(name="Horn", outcome_odds=Fraction(3, 1)) in throw_7
        assert OutcomeField(name="Field", outcome_odds=Fraction(1, 1)) in throw_7
        assert Outcome(name="Craps", outcome_odds=Fraction(7, 1)) in throw_7
