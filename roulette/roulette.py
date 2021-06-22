"""
TODO
"""

import random
from random import Random
from typing import Tuple, FrozenSet, Iterator


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

    def __init__(self, *outcomes: Outcome) -> None:
        """Create a frozenset containing all ``outcomes`` provided for this `Bin`.

        Args:
            outcomes: One or more Outcome instances to be added to this Bin.
        """
        self.outcomes = frozenset(outcomes)

    def add(self, *outcomes: Outcome) -> None:
        """Add any ``outcomes`` instance(s) provided as argument(s) to this `Bin`.

        Args:
            outcomes: One or more `Outcome` instances to add to this `Bin`.
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

    def add_outcome(self, number: int, outcome: Outcome) -> None:
        """Adds the given Outcome object to the Bin instance with the given number.

        Args:
            number: `Bin` ``number`` in the range zero to 37 inclusive.
            outcome: The `Outcome` to add to this `Bin`.
        """
        if 0 <= number <= 37:
            self.bins[number].add(outcome)
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
    
    def __init__(self) -> None:
        """Initialises the `BinBuilder`."""
        ...

    def build_bins(self, wheel: Wheel) -> None:
        """Creates the Outcome instances and uses the add_outcome() method to
        place each Outcome in the appropriate Bin of wheel."""
        ...




if __name__ == "__main__":
    w = Wheel()
    w.add_outcome(0, Outcome("0", 35))
    w.add_outcome(0, Outcome("0-00-1-2-3", 6))
    w.add_outcome(0, Outcome("0-00-1-2-3", 6))
    print(w.bins[0])
