"""
TODO
"""

import random
from random import Random
from typing import (
    Tuple,
    FrozenSet,
    Iterator,
    Iterable,
    Dict,
    List,
)

if __package__ is None or __package__ == "":
    # Uses current directory visibility when not running as a package.
    import odds
else:
    # Uses current package visibility when running as a package or with pytest.
    from . import odds


class Outcome:
    """`Outcome` contains a single outcome on which a bet can be placed.

    In Roulette, each spin of the wheel has a number of `Outcome objects with
    bets that will be paid off. For example, the “1” bin has the following
    winning Outcome instances: “1”, “Red”, “Odd”, “Low”, “Column 1”,
    “Dozen 1-12”, “Split 1-2”, “Split 1-4”, “Street 1-2-3”, “Corner 1-2-4-5”,
    “Five Bet”, “Line 1-2-3-4-5-6”, “00-0-1-2-3”, “Dozen 1”, “Low” and
    “Column 1”.

    All of thee above-named bets will pay off if the wheel spins a “1”. This
    makes a Wheel and a Bin fairly complex containers of Outcome objects.

    Attributes:
        name: The name of this `Outcome`. E.g. ``1``, ``Red``, ``Even`` or ``Low``.
        odds: The payout odds of this outcome. Most odds are stated as 1:1 or
            17:1, we only keep the numerator (17) and assume the denominator is 1.
    """

    def __init__(self, name: str, odds: int) -> None:
        """Sets the instance `name` and `odds` from the parameter `name` and
        `odds`.
        """
        self.name = name
        self.odds = odds

    def win_amount(self, amount: float) -> float:
        """Multiply this `Outcome`'s odds by the given ``amount``. The product is
        returned.

        Args:
            amount: The amount being bet.

        Returns:
            The amount in winnings excluding the initial bet.
        """
        return self.odds * amount

    def __eq__(self, other: object) -> bool:
        """Compare the `name` attributes of `self` and ``other``.

        Args:
            other: Another `Outcome` to compare against.

        Returns:
            True if this name matches the ``other``'s name, False otherwise.
        """
        if not isinstance(other, Outcome):
            return NotImplemented
        return self.name == other.name

    def __ne__(self, other: object) -> bool:
        """Compare the `name` attributes of `self` and ``other``.

        Args:
            other: Another `Outcome` to compare against.

        Returns:
            True if this name does not match the ``other``'s name, False otherwise.
        """
        if not isinstance(other, Outcome):
            return NotImplemented
        return self.name != other.name

    def __hash__(self) -> int:
        """Hash value for this outcome.

        Returns:
            The hash value of the name, ``hash(self.name)``.
        """
        return hash(self.name)

    def __str__(self) -> str:
        return f"{self.name} {self.odds}:1"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={repr(self.name)}, odds={repr(self.odds)})"
        )


class Bin(object):
    """`Bin` contains a collection of `Outcome` instances which reflect the winning
    bets that are paid for a particular bin on a Roulette wheel.

    In Roulette, each spin of the wheel has a number of `Outcome` instances.
    Example: A spin of 1, selects the “1” `Bin` with the following winning `Outcome`
    instances: “1”, “Red”, “Odd”, “Low”, “Column 1”, “Dozen 1-12”, “Split 1-2”,
    “Split 1-4”, “Street 1-2-3”, “Corner 1-2-4-5”, “Five Bet”, “Line 1-2-3-4-5-6”,
    “00-0-1-2-3”, “Dozen 1”, “Low” and “Column 1”. These are collected into a
    single `Bin`.

    Attributes:
        outcomes: A collection of `Outcome` instances.
    """

    outcomes: FrozenSet[Outcome]
    # TODO?: Subclassing set might be simpler than trying to work with frozenset.

    def __init__(self) -> None:
        """Create an empty `Bin` and initialise a frozenset to store added
        `Outcomes`.
        """
        self.outcomes = frozenset()

    def add(self, outcomes: Iterable[Outcome]) -> None:
        """Adds the given `Outcomes` to this `Bin`.

        Args:
            outcomes: An iterable containing one or more `Outcome` instances to
            add to this `Bin`.
        """
        self.outcomes |= frozenset(outcomes)

    def __iter__(self) -> Iterator:
        return iter(self.outcomes)

    def __contains__(self, item: Outcome) -> bool:
        return item in self.outcomes


class Wheel:
    """Wheel contains the 38 individual bins on a Roulette wheel, plus a random
    number generator. It can select a `Bin` at random, simulating a spin of the
    Roulette wheel.

    Attributes:
        bins: A tuple containing the 38 individual `bin` instances.
        rng: A random number generator to select a `Bin` from the `bins` collection.
    """

    bins: Tuple[Bin, ...]

    def __init__(self, rng: Random = None) -> None:
        """Creates a new wheel with 38 empty `Bin` instances. Also creates a
        new random number generator instance.
        TODO: Full initialization of the Bin instances.

        Args:
            rng: Optional; Provide a seeded `Random` instance for use in testing.
        """
        if rng is None:
            self.rng = random.Random()
        else:
            # Use seeded Random for testing.
            self.rng = rng

        self.bins = tuple(Bin() for i in range(38))

    def add_outcomes(self, number: int, outcomes: Iterable[Outcome]) -> None:
        """Adds the given `Outcomes` to the `Bin` instance with the given number.

        Args:
            number: `Bin` ``number`` in the range zero to 37 inclusive.
            outcomes: An iterable containing one or more `Outcome` instances to
            add to this `Bin`.
        """
        if 0 <= number <= 37:
            self.bins[number].add(outcomes)
        else:
            raise IndexError("'Number' must be between 0-37 inclusive.")

    def choose(self) -> Bin:
        """Randomly returns a `Bin` instance from the bins collection using the
        internal Random instance, rng.

        Returns:
            A `Bin` selected at random from the wheel.
        """
        return self.rng.choice(self.bins)

    def get(self, bin_num: int) -> Bin:
        """Return the given `Bin` instance from the internal collection.

        Args:
            bin_num: bin number, in the range 0-37 inclusive.

        Returns:
            The requested `Bin` instance.
        """
        return self.bins[bin_num]


class BinBuilder:
    """`BinBuilder` creates the `Outcome` instances for all of the 38 individual
    `Bin` on a Roulette wheel.
    """

    temp_bins: Dict[int, List[Outcome]]

    def __init__(self) -> None:
        """Initialises the `BinBuilder`."""
        self.temp_bins = {bin_num: list() for bin_num in range(0, 38)}

    def build_bins(self, wheel: Wheel) -> None:
        """Creates the `Outcome` instances and uses the add_outcome() method to
        place each `Outcome` in the appropriate `Bin` of `Wheel`."""
        self.gen_straight_bets()
        self.gen_split_bets()
        self.gen_street_bets()
        self.gen_corner_bets()
        self.gen_line_bets()
        self.gen_dozen_bets()
        self.gen_column_bets()
        self.gen_even_money_bets()
        self.gen_five_bets()

        for bin_num, outcomes in self.temp_bins.items():
            wheel.add_outcomes(bin_num, outcomes)

    def gen_straight_bets(self) -> None:
        """TODO"""
        for n in range(1, 37):
            outcome = Outcome(f"Number {n}", odds.STRAIGHT)
            self.temp_bins[n].append(outcome)
        self.temp_bins[0].append(Outcome(f"Number 0", odds.STRAIGHT))
        self.temp_bins[37].append(Outcome(f"Number 00", odds.STRAIGHT))

    def gen_split_bets(self) -> None:
        """TODO"""
        # Left-right split.
        for row in range(0, 12):
            n = row * 3 + 1
            outcome = Outcome(f"{n}-{n+1} Split", odds.SPLIT)
            self.temp_bins[n].append(outcome)
            self.temp_bins[n + 1].append(outcome)
            outcome = Outcome(f"{n+1}-{n+2} Split", odds.SPLIT)
            self.temp_bins[n + 1].append(outcome)
            self.temp_bins[n + 2].append(outcome)

        # Up-down split.
        for n in range(1, 34):
            outcome = Outcome(f"{n}-{n+3} Split", odds.SPLIT)
            self.temp_bins[n].append(outcome)
            self.temp_bins[n + 3].append(outcome)

    def gen_street_bets(self) -> None:
        """TODO"""
        for row in range(0, 12):
            n = row * 3 + 1
            outcome = Outcome(f"{n}-{n+1}-{n+2} Street", odds.STREET)
            self.temp_bins[n].append(outcome)
            self.temp_bins[n + 1].append(outcome)
            self.temp_bins[n + 2].append(outcome)

    def gen_corner_bets(self) -> None:
        """TODO"""
        for row in range(0, 11):
            n = row * 3 + 1
            # Left corner.
            outcome = Outcome(f"{n}-{n+1}-{n+3}-{n+4} Corner", odds.CORNER)
            self.temp_bins[n].append(outcome)
            self.temp_bins[n + 1].append(outcome)
            self.temp_bins[n + 3].append(outcome)
            self.temp_bins[n + 4].append(outcome)
            # Right corner.
            outcome = Outcome(f"{n+1}-{n+2}-{n+4}-{n+5} Corner", odds.CORNER)
            self.temp_bins[n + 1].append(outcome)
            self.temp_bins[n + 2].append(outcome)
            self.temp_bins[n + 4].append(outcome)
            self.temp_bins[n + 5].append(outcome)

    def gen_line_bets(self) -> None:
        """TODO"""
        for row in range(0, 11):
            n = row * 3 + 1
            outcome = Outcome(f"{n}-{n+1}-{n+2}-{n+3}-{n+4}-{n+5} Line", odds.LINE)
            self.temp_bins[n].append(outcome)
            self.temp_bins[n + 1].append(outcome)
            self.temp_bins[n + 2].append(outcome)
            self.temp_bins[n + 3].append(outcome)
            self.temp_bins[n + 4].append(outcome)
            self.temp_bins[n + 5].append(outcome)

    def gen_dozen_bets(self) -> None:
        """TODO"""
        for dozen in range(0, 3):
            outcome = Outcome(f"Dozen {dozen+1}", odds.DOZEN)
            for n in range(0, 12):
                self.temp_bins[dozen * 12 + n + 1].append(outcome)

    def gen_column_bets(self) -> None:
        """TODO"""
        for col in range(0, 3):
            outcome = Outcome(f"Column {col + 1}", odds.COLUMN)
            for row in range(0, 12):
                self.temp_bins[row * 3 + col + 1].append(outcome)

    def gen_even_money_bets(self):
        """Red, black, even, odd, high, low.
        TODO
        """
        red_o = Outcome("Red", odds.EVEN)
        black_o = Outcome("Black", odds.EVEN)
        even_o = Outcome("Even", odds.EVEN)
        odd_o = Outcome("Odd", odds.EVEN)
        high_o = Outcome("High", odds.EVEN)
        low_o = Outcome("Low", odds.EVEN)

        for n in range(1, 37):
            if 1 <= n < 19:
                self.temp_bins[n].append(low_o)
            else:
                self.temp_bins[n].append(high_o)
            if n % 2 == 0:
                self.temp_bins[n].append(even_o)
            else:
                self.temp_bins[n].append(odd_o)
            if n in {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}:
                self.temp_bins[n].append(red_o)
            else:
                self.temp_bins[n].append(black_o)

    def gen_five_bets(self) -> None:
        """TODO"""
        outcome = Outcome("Five", odds.FIVE)
        for n in [0, 37, 1, 2, 3]:
            self.temp_bins[n].append(outcome)





if __name__ == "__main__":
    w = Wheel()
    builder = BinBuilder()
    builder.build_bins(w)
    for i in range(10):
        print("hi")
