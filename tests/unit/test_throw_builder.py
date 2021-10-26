from collections import Counter
from fractions import Fraction

import pytest

# Different import style here than rest of project because it made the file _so_ ugly.
from casino.main import (
    CrapsThrow,
    NaturalThrow,
    ElevenThrow,
    PointThrow,
    Outcome,
    OutcomeField,
    OutcomeHorn,
)


@pytest.mark.usefixtures("built_dice")
class TestThrowBuilder:
    def test_correct_throw_object(self, built_dice):
        for k, v in built_dice.throws.items():
            key_sum = sum(k)
            if key_sum in {2, 3, 12}:
                assert isinstance(v, CrapsThrow)
            elif key_sum == 7:
                assert isinstance(v, NaturalThrow)
            elif key_sum == 11:
                assert isinstance(v, ElevenThrow)
            else:
                assert isinstance(v, PointThrow)

    def test_correct_number_win_one_roll_outcomes(self, built_dice):
        count = Counter(
            [
                outcome.name
                for sublist in list(built_dice.throws.values())
                for outcome in sublist.win_one_roll
            ]
        )
        # assert there are x many winning one roll outcomes for count.get(proposition).
        assert count.get("Proposition 2") == 1
        assert count.get("Field") == 16
        assert count.get("Craps") == 4
        assert count.get("Horn") == 6
        assert count.get("Proposition 3") == 2
        assert count.get("Proposition 7") == 6
        assert count.get("Proposition 11") == 2
        assert count.get("Proposition 12") == 1
        assert count.get("Hard 4") is None
        assert count.get("Hard 6") is None
        assert count.get("Hard 8") is None
        assert count.get("Hard 10") is None

    def test_correct_number_lose_one_roll_outcomes(self, built_dice):
        count = Counter(
            [
                outcome.name
                for sublist in list(built_dice.throws.values())
                for outcome in sublist.lose_one_roll
            ]
        )
        # assert there are x many losing one roll outcomes for count.get(proposition).
        assert count.get("Proposition 11") == 34
        assert count.get("Proposition 12") == 35
        assert count.get("Proposition 7") == 30
        assert count.get("Proposition 3") == 34
        assert count.get("Proposition 2") == 35
        assert count.get("Horn") == 30
        assert count.get("Craps") == 32
        assert count.get("Field") == 20
        assert count.get("Hard 4") is None
        assert count.get("Hard 6") is None
        assert count.get("Hard 8") is None
        assert count.get("Hard 10") is None

    def test_correct_number_win_hardways_outcomes(self, built_dice):
        count = Counter(
            [
                outcome.name
                for sublist in list(built_dice.throws.values())
                for outcome in sublist.win_hardway
            ]
        )
        # assert there are x many winning hardways outcomes for count.get(proposition).
        assert count.get("Hardways 4") == 1
        assert count.get("Hardways 6") == 1
        assert count.get("Hardways 8") == 1
        assert count.get("Hardways 10") == 1
        assert count.get("Proposition 11") is None
        assert count.get("Proposition 12") is None
        assert count.get("Proposition 7") is None
        assert count.get("Proposition 3") is None
        assert count.get("Proposition 2") is None
        assert count.get("Horn") is None
        assert count.get("Craps") is None
        assert count.get("Field") is None

    def test_correct_number_lose_hardways_outcomes(self, built_dice):
        count = Counter(
            [
                outcome.name
                for sublist in list(built_dice.throws.values())
                for outcome in sublist.lose_hardway
            ]
        )
        # assert there are x many losing hardways outcomes for count.get(proposition).
        assert count.get("Hardways 4") == 8
        assert count.get("Hardways 6") == 10
        assert count.get("Hardways 8") == 10
        assert count.get("Hardways 10") == 8
        assert count.get("Proposition 11") is None
        assert count.get("Proposition 12") is None
        assert count.get("Proposition 7") is None
        assert count.get("Proposition 3") is None
        assert count.get("Proposition 2") is None
        assert count.get("Horn") is None
        assert count.get("Craps") is None
        assert count.get("Field") is None

    def test_random_sample_throws(self, built_dice):
        throw_1 = built_dice.throws.get((1, 1)).win_one_roll
        assert len(throw_1) == 4
        assert Outcome(name="Proposition 2", outcome_odds=Fraction(30, 1)) in throw_1
        assert OutcomeHorn(name="Horn", outcome_odds=Fraction(3, 1)) in throw_1
        assert OutcomeField(name="Field", outcome_odds=Fraction(1, 1)) in throw_1
        assert Outcome(name="Craps", outcome_odds=Fraction(7, 1)) in throw_1

        throw_2 = built_dice.throws.get((1, 3)).lose_one_roll
        assert len(throw_2) == 7
        assert Outcome(name="Craps", outcome_odds=Fraction(7, 1)) in throw_2
        assert Outcome(name="Proposition 7", outcome_odds=Fraction(4, 1)) in throw_2
        assert Outcome(name="Proposition 11", outcome_odds=Fraction(15, 1)) in throw_2
        assert Outcome(name="Proposition 2", outcome_odds=Fraction(30, 1)) in throw_2
        assert Outcome(name="Proposition 12", outcome_odds=Fraction(30, 1)) in throw_2
        assert Outcome(name="Proposition 3", outcome_odds=Fraction(15, 1)) in throw_2
        assert OutcomeHorn(name="Horn", outcome_odds=Fraction(3, 1)) in throw_2

        throw_3 = built_dice.throws.get((3, 3)).win_hardway
        assert len(throw_3) == 1
        assert Outcome(name="Hardways 6", outcome_odds=Fraction(9, 1)) in throw_3

        throw_4 = built_dice.throws.get((4, 3)).lose_hardway
        assert len(throw_4) == 4
        assert Outcome(name="Hardways 6", outcome_odds=Fraction(9, 1)) in throw_4
        assert Outcome(name="Hardways 10", outcome_odds=Fraction(7, 1)) in throw_4
        assert Outcome(name="Hardways 4", outcome_odds=Fraction(7, 1)) in throw_4
        assert Outcome(name="Hardways 8", outcome_odds=Fraction(9, 1)) in throw_4

        throw_5 = built_dice.throws.get((4, 6)).winners
        assert len(throw_5) == 1
        assert OutcomeField(name="Field", outcome_odds=Fraction(1, 1)) in throw_5

        throw_6 = built_dice.throws.get((5, 6)).losers
        assert len(throw_6) == 5
        assert Outcome(name="Craps", outcome_odds=Fraction(7, 1)) in throw_6
        assert Outcome(name="Proposition 7", outcome_odds=Fraction(4, 1)) in throw_6
        assert Outcome(name="Proposition 2", outcome_odds=Fraction(30, 1)) in throw_6
        assert Outcome(name="Proposition 12", outcome_odds=Fraction(30, 1)) in throw_6
        assert Outcome(name="Proposition 3", outcome_odds=Fraction(15, 1)) in throw_6

        throw_7 = built_dice.throws.get((6, 6)).outcomes
        assert len(throw_7) == 0
