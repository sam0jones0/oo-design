"""
TODO
"""
import csv
import math
import random
import typing
from fractions import Fraction
from typing import (
    Tuple,
    FrozenSet,
    Iterator,
    Iterable,
    Optional,
    Dict,
    List,
    Type,
    Union,
)

if __package__ is None or __package__ == "":
    # Use current directory visibility when not running as a package.
    import odds
else:
    # Use current package visibility when running as a package or with pytest.
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
        outcome_odds: The payout odds of this outcome. Most odds are stated as 1:1 or
            17:1. Either the numerator (17) is provided and the denominator is
            assumed to be 1, or an exact `Fraction` object of the odds is provided.
    """

    def __init__(self, name: str, outcome_odds: Union[Fraction, int]) -> None:
        """Sets the instance `name` and `odds` from the parameters. An appropriate
        `Fraction` to represent the odds is created.
        """
        self.name = name
        if isinstance(outcome_odds, int):
            self.odds = Fraction(outcome_odds, 1)
        elif isinstance(outcome_odds, Fraction):
            self.odds = outcome_odds
        else:
            raise TypeError("outcome_odds must be either an int or Fraction.")

    def win_amount(self, amount: int) -> int:
        """Multiplies this `Outcome`'s odds by the given ``amount`` and returns
        the product.

        Args:
            amount: The amount being bet.

        Returns:
            The amount in winnings as an `int` excluding the initial bet.
        """
        return int(self.odds * amount)

    def __eq__(self, other: object) -> bool:
        """Compares the `name` attributes of `self` and ``other``.

        Args:
            other: Another `Outcome` to compare against.

        Returns:
            True if this name matches the ``other``'s name, False otherwise.
        """
        if not isinstance(other, Outcome):
            return NotImplemented
        return self.name == other.name

    def __ne__(self, other: object) -> bool:
        """Compares the `name` attributes of `self` and ``other``.

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
        return f"{self.name} {self.odds.numerator}:{self.odds.denominator}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={repr(self.name)}, odds={repr(self.odds)})"
        )


class Bin:
    """`Bin` contains a collection of `Outcome` instances which reflect the winning
    bets that are paid for a particular bin on a Roulette wheel.

    In Roulette, each spin of the wheel has a number of `Outcome` instances.
    Example: A spin of 1, selects the “1” `Bin` with the following winning `Outcome`
    instances: “1”, “Red”, “Odd”, “Low”, “Column 1”, “Dozen 1-12”, “Split 1-2”,
    “Split 1-4”, “Street 1-2-3”, “Corner 1-2-4-5”, “Five Bet”, “Line 1-2-3-4-5-6”,
    “00-0-1-2-3”, “Dozen 1”, “Low” and “Column 1”. These are collected into a
    single `Bin`.

    Attributes:
        outcomes: A collection of `Outcome` instances in this `Bin`.
    """

    outcomes: FrozenSet[Outcome]

    def __init__(self) -> None:
        """Creates an empty `Bin` and initialise a frozenset to store added
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


class Throw:
    """The `Throw` class is the superclass for the various throws of the dice.

    Each subclass is a different grouping of the numbers, based on the rules for
    Craps.

    Attributes:
        d1: One of the two die values, from 1 to 6.
        d2: The other of the two die values, from 1 to 6.
        outcomes: A `frozenset` of one-roll `Outcomes` that win with this throw.
            These bets are immediately resolved as winners.
        key: The key for this `Throw`. E.g. to locate the `Throw` object in dict
        collections of all throws, such as `Dice.throws`.
    """

    key: Tuple[int, int]

    def __init__(self, d1: int, d2: int, *outcomes: Outcome) -> None:
        """Creates this throw, and associates the given `Outcome` instances that
        are winning propositions.
        """
        self.d1 = d1
        self.d2 = d2
        self.outcomes = frozenset(outcomes)
        self.key = (d1, d2)

    def hard(self) -> bool:
        """Helps to determine if hardways bets have been won or lost.

        Returns:
            `True` if d1 is equal to d2, `False` otherwise.
        """
        return self.d1 == self.d2

    def update_game(self, game: "CrapsGame") -> None:
        """Calls one of the `CrapsGame` state change methods: craps(), natural(),
        eleven() or point(). This may change the game state and resolve bets.

        Args:
            game: The `CrapsGame` object to be updated based on this throw.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.d1}, {self.d2}"


class NaturalThrow(Throw):
    """`Throw` subclass for the 'natural' number, 7.

    Attributes:
        outcomes: A `frozenset` of one-roll `Outcomes` that win with this throw.
            These bets are immediately resolved as winners.
        d1: One of the two die values, from 1 to 6.
        d2: The other of the two die values, from 1 to 6.
    """

    def __init__(self, d1: int, d2: int, *outcomes: Outcome) -> None:
        """Creates this `Throw` instance providing the constraint ``d1`` + ``d2`` == 7 is
        satisfied.

        Raises:
            ValueError: Values of d1 and d2 do not represent a `NaturalThrow`.
        """
        if d1 + d2 != 7:
            raise ValueError("d1 + d2 must == 7 to init a NaturalThrow.")

        super(NaturalThrow, self).__init__(d1, d2, *outcomes)

    def hard(self) -> bool:
        """A natural 7 is odd, and can never be made hardways.

        Returns:
            False: Always.
        """
        return False

    def update_game(self, game: "CrapsGame") -> None:
        """Calls the natural() method of a `CrapsGame`. This may change the game
        state and resolve bets.

        Args:
            game: The `CrapsGame` to be updated based on this throw.
        """
        game.natural()


class CrapsThrow(Throw):
    """`Throw` subclass for the 'craps' numbers: 2, 3 and 12.

    Attributes:
        outcomes: A `frozenset` of one-roll `Outcomes` that win with this throw.
            These bets are immediately resolved as winners.
        d1: One of the two die values, from 1 to 6.
        d2: The other of the two die values, from 1 to 6.
    """

    def __init__(self, d1: int, d2: int, *outcomes: Outcome) -> None:
        """Creates this `Throw` instance providing the constraint ``d1`` + ``d2`` in {2, 3, 12}
        is satisfied.

        Raises:
            ValueError: Values of d1 and d2 do not represent a `CrapsThrow`.
        """
        if d1 + d2 not in {2, 3, 12}:
            raise ValueError("d1 + d2 must be in {2, 3, 12} to init a CrapsThrow.")

        super(CrapsThrow, self).__init__(d1, d2, *outcomes)

    def hard(self) -> bool:
        """Craps numbers are never part of hardways bets

        Returns:
            False: Always.
        """
        return False

    def update_game(self, game: "CrapsGame") -> None:
        """Calls the craps() method of a `CrapsGame` instance. This may change the
        game state and resolve bets.

        Args:
            game: The `CrapsGame` to be updated based on this throw.
        """
        game.craps()


class ElevenThrow(Throw):
    """`Throw` subclass for the number 11.

    This special throw has one effect on a come-out roll and a different effect
    on point rolls.

    Attributes:
        outcomes: A `frozenset` of one-roll `Outcomes` that win with this throw.
            These bets are immediately resolved as winners.
        d1: One of the two die values, from 1 to 6.
        d2: The other of the two die values, from 1 to 6.
    """

    def __init__(self, d1: int, d2: int, *outcomes: Outcome) -> None:
        """Creates this `Throw` instance providing the constraint ``d1`` + ``d2`` == 11
        is satisfied.

        Raises:
            ValueError: Values of d1 and d2 do not represent an `ElevenThrow`.
        """
        if d1 + d2 != 11:
            raise ValueError("d1 + d2 must == 11 to init an ElevenThrow.")

        super(ElevenThrow, self).__init__(d1, d2, *outcomes)

    def hard(self) -> bool:
        """Eleven is odd and is never part of hardways bets.

        Returns:
            False: Always.
        """
        return False

    def update_game(self, game: "CrapsGame") -> None:
        """Calls the eleven() method of a `CrapsGame` instance. This may change the
        game state and resolve bets.

        Args:
            game: The `CrapsGame` to be updated based on this throw.
        """
        game.eleven()


class PointThrow(Throw):
    """`Throw` subclass for the point numbers: 4, 5, 6, 8, 9 and 10.

    Attributes:
        outcomes: A `frozenset` of one-roll `Outcomes` that win with this throw.
            These bets are immediately resolved as winners.
        d1: One of the two die values, from 1 to 6.
        d2: The other of the two die values, from 1 to 6.
    """

    def __init__(self, d1: int, d2: int, *outcomes: Outcome) -> None:
        """Creates this `Throw` instance providing the constraint ``d1`` + ``d2`` in
        {4, 5, 6, 8, 9, 10} is satisfied."""
        if d1 + d2 not in {4, 5, 6, 8, 9, 10}:
            raise ValueError(
                "d1 + d2 must be in {4, 5, 6, 8, 9, 10} to init a PointThrow."
            )

        super(PointThrow, self).__init__(d1, d2, *outcomes)

    def update_game(self, game: "CrapsGame") -> None:
        """Calls the point() method of a `CrapsGame` instance. This may change the
        game state and resolve bets.

        Args:
            game: The `CrapsGame` to be updated based on this throw.
        """
        game.point()


class Dice:
    """A `Dice` instances contains the 36 individual throws of two dice, plus
    a random number generator. It can select a `Throw` object at random,
    simulating a throw of dice.

    Attributes:
        throws: A `dict` that maps a two-tuple (`Throw.key`) to a `Throw` instance.
        rng: A random number generator used to select a `Throw` instance from
            the `throws` collection.
    """

    throws: Dict[Tuple[int, int], Throw]

    def __init__(self) -> None:
        """Build the dictionary of `Throw` instances."""
        self.throws = dict()  # TODO: Build `Throw` objects.
        self.rng = random.Random()

    def add_throw(self, throw: Throw) -> None:
        """Adds the given `Throw` to the mapping maintained by this `Dice`
        instance.

        Args:
            throw: The `Throw` to add.
        """
        self.throws[throw.key] = throw

    def roll(self) -> Throw:
        """Returns a randomly selected `Throw` instance."""
        result_key = self.rng.choice(list(self.throws))
        return self.throws[result_key]

    def _get_throw(self, d1: int, d2: int) -> Optional[Throw]:
        """Takes a particular combination of dice and returns the appropriate
        `Throw` object.

        This is not needed by the main application. Unit tests will need this method
        to return a specific `Throw` rather than a randomly selected one.

        Args:
            d1: The value of one die.
            d2: The value of the other die.

        Returns:
            The specified `Throw` instance. Or `None` if no such instance exists.
        """
        return self.throws.get((d1, d2))


class Wheel:
    """Wheel contains the 38 individual bins on a Roulette wheel, a random
    number generator and a collection of all possible outcomes. It can select a
    `Bin` at random, simulating a spin of the Roulette wheel.

    Attributes:
        bins: A tuple containing the 38 individual `bin` instances.
        rng: A random number generator to select a `Bin` from the `bins` collection.
        all_outcomes: A dict containing all possible outcomes.
    """

    bins: Tuple[Bin, ...]
    all_outcomes: Dict[str, Outcome]

    def __init__(self) -> None:
        """Creates a new wheel with 38 empty `Bin` instances and then calls on
        `BinBuilder` to populate them. Also creates a new random number
        generator instance and a dict to store all possible outcomes.
        """
        self.bins = tuple(Bin() for _ in range(38))
        self.all_outcomes = dict()
        self.rng = random.Random()
        self.bin_builder = BinBuilder()
        self.bin_builder.build_bins(self)

    def add_outcomes(self, number: int, outcomes: Iterable[Outcome]) -> None:
        """Adds the given `Outcomes` to the `Bin` instance with the given number
        and update the internal collection of all_outcomes.

        Args:
            number: `Bin` ``number`` in the range zero to 37 inclusive.
            outcomes: An iterable containing one or more `Outcome` instances to
            add to this `Bin`.

        Raises:
            IndexError: Invalid bin number.
        """
        if 0 <= number <= 37:
            self.bins[number].add(outcomes)
            self.all_outcomes.update(
                {outcome.name.lower(): outcome for outcome in outcomes}
            )
        else:
            raise IndexError("'Number' must be between 0-37 inclusive.")

    def choose(self) -> Bin:
        """Randomly returns a `Bin` instance from the bins collection using the
        internal Random instance, rng.

        Returns:
            A `Bin` selected at random from the wheel.
        """
        return self.rng.choice(self.bins)

    def get_bin(self, bin_num: int) -> Bin:
        """Returns the given `Bin` instance from the internal collection.

        Args:
            bin_num: bin number, in the range 0-37 inclusive.

        Returns:
            The requested `Bin` instance.
        """
        return self.bins[bin_num]

    def get_outcome(self, name: str) -> Outcome:
        """Returns an `Outcome` instance given the string ``name`` of the `Outcome`
        from an internal collection of all_outcomes.

        Args:
            name: The name of an `Outcome`

        Returns:
            The requested `Outcome` instance.

        Raises:
            KeyError: There is no `Outcome` with name: ``name``.
        """
        outcome = self.all_outcomes.get(name.lower())
        if outcome is None:
            raise KeyError(f"No Outcome with name: {name}")
        return outcome


class BinBuilder:
    """`BinBuilder` creates the `Outcome` instances for all of the 38 individual
    `Bin`s on a Roulette wheel.

    Each gen_* method enumerates the `Outcomes` for each type of bet.

    Attributes:
        temp_bins: Interim collection of `Outcome` instances associated with bin
            numbers that will be used to populate the final `Bin` objects assigned
            to the `Wheel`.
    """

    temp_bins: Dict[int, List[Outcome]]

    def __init__(self) -> None:
        """Initialise the `BinBuilder`."""
        self.temp_bins = {bin_num: list() for bin_num in range(0, 38)}

    def build_bins(self, wheel: Wheel) -> None:
        """Creates the `Outcome` instances associated with each type of bet and
        use the `Wheel`'s `add_outcome()` method to place each `Outcome` in the
        appropriate `Bin`.

        Args:
            wheel: The `Wheel` with `Bins` that must be populated with the
                `Outcome` instances.
        """
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
        for num in range(1, 37):
            outcome = Outcome(f"Number {num}", odds.STRAIGHT)
            self.temp_bins[num].append(outcome)
        self.temp_bins[0].append(Outcome("Number 0", odds.STRAIGHT))
        self.temp_bins[37].append(Outcome("Number 00", odds.STRAIGHT))

    def gen_split_bets(self) -> None:
        # Left-right split.
        for row in range(0, 12):
            num = row * 3 + 1
            outcome = Outcome(f"{num}-{num + 1} Split", odds.SPLIT)
            self.temp_bins[num].append(outcome)
            self.temp_bins[num + 1].append(outcome)
            outcome = Outcome(f"{num + 1}-{num + 2} Split", odds.SPLIT)
            self.temp_bins[num + 1].append(outcome)
            self.temp_bins[num + 2].append(outcome)

        # Up-down split.
        for num in range(1, 34):
            outcome = Outcome(f"{num}-{num + 3} Split", odds.SPLIT)
            self.temp_bins[num].append(outcome)
            self.temp_bins[num + 3].append(outcome)

    def gen_street_bets(self) -> None:
        for row in range(0, 12):
            num = row * 3 + 1
            outcome = Outcome(f"{num}-{num + 1}-{num + 2} Street", odds.STREET)
            self.temp_bins[num].append(outcome)
            self.temp_bins[num + 1].append(outcome)
            self.temp_bins[num + 2].append(outcome)

    def gen_corner_bets(self) -> None:
        for row in range(0, 11):
            num = row * 3 + 1
            # Left corner.
            outcome = Outcome(
                f"{num}-{num + 1}-{num + 3}-{num + 4} Corner", odds.CORNER
            )
            self.temp_bins[num].append(outcome)
            self.temp_bins[num + 1].append(outcome)
            self.temp_bins[num + 3].append(outcome)
            self.temp_bins[num + 4].append(outcome)
            # Right corner.
            outcome = Outcome(
                f"{num + 1}-{num + 2}-{num + 4}-{num + 5} Corner", odds.CORNER
            )
            self.temp_bins[num + 1].append(outcome)
            self.temp_bins[num + 2].append(outcome)
            self.temp_bins[num + 4].append(outcome)
            self.temp_bins[num + 5].append(outcome)

    def gen_line_bets(self) -> None:
        for row in range(0, 11):
            num = row * 3 + 1
            outcome = Outcome(
                f"{num}-{num + 1}-{num + 2}-{num + 3}-{num + 4}-{num + 5} Line",
                odds.LINE,
            )
            self.temp_bins[num].append(outcome)
            self.temp_bins[num + 1].append(outcome)
            self.temp_bins[num + 2].append(outcome)
            self.temp_bins[num + 3].append(outcome)
            self.temp_bins[num + 4].append(outcome)
            self.temp_bins[num + 5].append(outcome)

    def gen_dozen_bets(self) -> None:
        for dozen in range(0, 3):
            outcome = Outcome(f"Dozen {dozen+1}", odds.DOZEN)
            for num in range(0, 12):
                self.temp_bins[dozen * 12 + num + 1].append(outcome)

    def gen_column_bets(self) -> None:
        for col in range(0, 3):
            outcome = Outcome(f"Column {col + 1}", odds.COLUMN)
            for row in range(0, 12):
                self.temp_bins[row * 3 + col + 1].append(outcome)

    def gen_even_money_bets(self):
        red_o = Outcome("Red", odds.EVEN)
        black_o = Outcome("Black", odds.EVEN)
        even_o = Outcome("Even", odds.EVEN)
        odd_o = Outcome("Odd", odds.EVEN)
        high_o = Outcome("High", odds.EVEN)
        low_o = Outcome("Low", odds.EVEN)

        for num in range(1, 37):
            if 1 <= num < 19:
                self.temp_bins[num].append(low_o)
            else:
                self.temp_bins[num].append(high_o)
            if num % 2 == 0:
                self.temp_bins[num].append(even_o)
            else:
                self.temp_bins[num].append(odd_o)
            if num in {
                1,
                3,
                5,
                7,
                9,
                12,
                14,
                16,
                18,
                19,
                21,
                23,
                25,
                27,
                30,
                32,
                34,
                36,
            }:
                self.temp_bins[num].append(red_o)
            else:
                self.temp_bins[num].append(black_o)

    def gen_five_bets(self) -> None:
        outcome = Outcome("Five", odds.FIVE)
        for num in [0, 37, 1, 2, 3]:
            self.temp_bins[num].append(outcome)


class Bet:
    """A `Bet` on a specific `Outcome`.

    Maintains an association between an amount wagered, an `Outcome` object, and
    the specific `Player` who made the `Bet`.

    Attributes:
        amount: The amount of the bet.
        outcome: The `Outcome` we're betting on.
    """

    def __init__(self, amount: int, outcome: Outcome) -> None:
        """Creates a new `Bet` of a specific ``amount`` on a specific ``outcome``."""
        self.amount = amount
        self.outcome = outcome

    def win_amount(self) -> int:
        """Returns total winnings for this `Bet`, including initial bet `amount`."""
        return self.outcome.win_amount(self.amount) + self.amount

    def __str__(self) -> str:
        return f"{self.amount} on {self.outcome}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={repr(self.amount)}, outcome={repr(self.outcome)})"


class InvalidBet(Exception):
    """Raised when a `Player` instances attempts to place a bet outside the
    minimum/maximum limits.
    """

    pass


class Table:
    """`Table` contains all the `Bet` instances created by a `Player` object.
    A table also has a betting limit, and the sum of all a player's bets must be
    less than or equal to this limit. We assume a single `Player` object in the
    simulation.

    Attributes:
        limit: This is the table limit. The sum of the bets from a `Player` object
            must be less than or equal to this limit.
        bets: This is a list of the `Bet` instances currently active. These will
            result in either wins or losses to the `Player` object.
        bets_total: A running total of all `Bet`'s amounts in play.
    """

    bets: List[Bet]
    limit: int
    bets_total: int

    def __init__(self, *bets: Bet) -> None:
        """Creates an empty list of bets."""
        self.bets = []
        self.bets_total = 0
        self.limit = 30
        self.wheel = Wheel()

        if bets is not None:
            for bet in bets:
                self.place_bet(bet)

    def place_bet(self, bet: Bet) -> None:
        """Adds this ``bet`` to the list of active `bets` after checking if placing
        this bet does not violate the `Table` bet limit rules.

        Args:
            bet: A `Bet` instances to be added to the table.

        Raises:
            InvalidBet: Placing this ``bet`` breaks the `Table` limit rules.
        """
        if 0 < bet.amount <= self.limit and self.bets_total + bet.amount <= self.limit:
            self.bets.append(bet)
            self.bets_total += bet.amount
        else:
            raise InvalidBet("Placing this bet violates table min/limit rules.")

    def validate(self) -> bool:
        """Confirms the table-limit rules have been adhered to such that the sum
        of all bets is no greater than `self.limit`.

        Returns:
            True, if `Table` state is valid.

        Raises:
            InvalidBet: The bets don't pass the `Table` limit rules.
        """
        total_amount = 0
        for bet in self.bets:
            total_amount += bet.amount
            if not (0 < bet.amount <= self.limit and total_amount <= self.limit):
                raise InvalidBet("Active bets violate the table limit rules.")
        return True

    def clear(self) -> None:
        """Clears the table of all `Bet` instances, to be called once `Game` has resolved
        all `Bet`'s."""
        self.bets = []
        self.bets_total = 0

    def __iter__(self) -> Iterator[Bet]:
        """Returns an iterator over the available `Bet` instances."""
        # We need to be able remove bets from the table. Consequently, we have
        # to update the list, which requires we create a copy of the list.
        return iter(self.bets[:])

    def __str__(self) -> str:
        return ", ".join(str(bet) for bet in self.bets)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(repr(bet) for bet in self.bets)})"


class Player:
    """`Player` places bets in Roulette.

    This is an abstract class, with no body for the `Player.place_bets()` method.
    However, this class does implement the basic `Player.win()` method used by
    all subclasses.

    Attributes:
        stake: The player's current stake represented as multiples of the table's
            minimum bet. Set to the player's starting budget by the overall
            simulation control.
        rounds_to_go: Number of rounds left to play. Set by the overall
            simulation control to the maximum number of rounds to play.
        table: The `Table` object used to place individual `Bet` instances. The
            `Table` object contains the `Wheel` object from which the player can
            get `Outcome` objects used to build `Bet` instances.
    """

    stake: int
    rounds_to_go: int

    def __init__(self, table: Table) -> None:
        """Constructs the `Player` instance with a specific `Table` object for
        placing `Bet` instances.
        """
        self.table = table
        self.stake = 0
        self.rounds_to_go = 0

    def reset(self, duration: int, stake: int) -> None:
        """Sets `stake` and `rounds_to_go` according to the values passed by the
        overall simulation control. Called before the start of a new session.

        Args:
            duration: The number of `rounds_to_go` for the next session.
            stake: The initial stake to begin the next session with.
        """
        self.rounds_to_go = duration
        self.stake = stake

    def place_bets(self) -> None:
        """Must be overridden in subclass as each `Player` will have different
        betting strategy.
        """
        raise NotImplementedError

    def playing(self) -> bool:
        """Returns ``True`` while the player is still active."""
        if self.rounds_to_go > 0 and self.stake > 0:
            return True
        else:
            return False

    def win(self, bet: Bet) -> None:
        """Notification from the `Game` object that the `Bet` instance was a
        winner. Increases `Player.stake` accordingly.

        Args:
              bet: The `Bet` which won.
        """
        self.stake += bet.win_amount()

    def lose(self, bet: Bet) -> None:
        """Notification from the `Game` object that the `Bet` instance was a loser.

        Does nothing by default, some subclassed players will take particular actions
        on losses.
        """
        pass

    def winners(self, outcomes: FrozenSet[Outcome]) -> None:
        """This is notification from the `Game` class of all the winning outcomes.
        Some subclasses will process this information.

        Args:
            outcomes: The `Outcome` set from a `Bin`.
        """
        pass


class Passenger57(Player):
    """Simple `Player` subclass who always constructs a `Bet` instance based on
    the `Outcome` object named 'Black'.

    Attributes:
        table: The `Table` that is used to place individual `Bet` instances.
        black: The `Outcome` on which this player focuses their betting.
    """

    black: Outcome

    def __init__(self, table: Table) -> None:
        """Constructs the `Player` instance with a specific `Table` and `Wheel
        for creating and resolving bets. Also creates the 'black' `Outcome` for
        use in creating bets.
        """
        super().__init__(table)
        self.black = table.wheel.get_outcome("black")

    def reset(self, duration: int, stake: int) -> None:
        """Calls parent class reset method.

        Args:
            duration: The number of `rounds_to_go` for the next session.
            stake: The initial stake to begin the next session with.
        """
        super(Passenger57, self).reset(duration, stake)

    def place_bets(self) -> None:
        """Create and place one `Bet` on the 'Black' `Outcome` instance."""
        current_bet = Bet(1, self.black)  # Stake will be >= 1 if self.playing()
        self.table.place_bet(current_bet)
        self.stake -= current_bet.amount


class Martingale(Player):
    """`Martingale` is a `Player` who places bets in Roulette. This player doubles
    their bet on every loss and resets their bet to a base amount on each win.

    Attributes:
        table: The `Table` that is used to place individual `Bet` instances.
        loss_count: The number of losses. This is the number of times to double
            the bet.
        bet_multiple: The bet multiplier, based on the number of losses. This
            starts at 1, and is reset to 1 on each win. It is doubled with each
            loss. This is always equal to 2**`loss_count`.
    """

    bet_multiple: int
    loss_count: int

    def __init__(self, table: Table) -> None:
        super().__init__(table)
        self.bet_multiple = 1  # TODO: Is this needed?
        self.loss_count = 0

    def reset(self, duration: int, stake: int) -> None:
        """Calls parent class reset method and also resets `Martingale` specific
        attributes for a new session.

        Args:
            duration: The number of `rounds_to_go` for the next session.
            stake: The initial stake to begin the next session with.
        """
        super(Martingale, self).reset(duration, stake)
        self.bet_multiple = 1
        self.loss_count = 0

    def place_bets(self) -> None:
        """Updates the `Table` object with a bet on 'black'. The amount bet is
        2**`loss_count`, which is the value of `bet_multiple`.

        If `bet_amount` exceeds `self.stake`, bet entire remaining stake. If
        `bet_amount` exceeds `table.limit`, restart the betting strategy.
        """
        bet_amount = 1 * (2 ** self.loss_count)
        if bet_amount > self.stake:
            bet_amount = self.stake
        current_bet = Bet(bet_amount, self.table.wheel.get_outcome("black"))
        try:
            self.table.place_bet(current_bet)
        except InvalidBet:
            self.reset(self.rounds_to_go, self.stake)
            self.place_bets()
            return
        self.stake -= current_bet.amount

    def win(self, bet: Bet) -> None:
        """Uses the superclass `Player.win()` method to update the stake with an
        amount won. Then resets `loss_count` to zero and resets `bet_multiple`
        to 1.

        Args:
            bet: The winning bet.
        """
        super(Martingale, self).win(bet)
        self.loss_count = 0
        self.bet_multiple = 1

    def lose(self, bet: Bet) -> None:
        """Uses the superclass `Player.loss()` to do whatever bookkeeping the
        superclass already does. Increments `loss_count` by 1 and doubles
        `bet_multiple`.

        Args:
            bet: The losing bet.
        """
        super(Martingale, self).lose(bet)
        self.loss_count += 1
        self.bet_multiple *= 2


class SevenReds(Martingale):
    """This is a `Martingale` player who places bets in roulette. They wait until
    the wheel has spun red seven times in a row before betting on black.

    Attributes:
        table: The `Table` that is used to place individual `Bet` instances.
        red_count: The number of reds yet to go. Inits to 7, and is reset to 7 on
            each non-red outcome, and decrements by 1 on each red outcome.
    """

    def __init__(self, table: Table) -> None:
        """Initialise parent class attributes and set `red_count` to it's starting
        value of 7.
        """
        super().__init__(table)
        self.red_count = 7

    def place_bets(self) -> None:
        """Places a bet on black using the Martingale betting system if we have
        seen seven reds in a row.
        """
        if self.red_count == 0:
            super(SevenReds, self).place_bets()

    def winners(self, outcomes: FrozenSet[Outcome]) -> None:
        """This is notification from the `Game` class of all the winning outcomes.
        If this includes red, then `red_count` is decremented. Otherwise, `red_count`
        is reset to 7.

        Args:
            outcomes: The `Outcome` set from a `Bin`.
        """
        if self.table.wheel.get_outcome("red") in outcomes:
            self.red_count -= 1
        else:
            self.red_count = 7


class PlayerRandom(Player):
    """A `Player` who places bets in roulette. This player makes random bets
    around the layout.

    Attributes:
        rng: A random number generator for selecting outcomes to bet on.
        table: The `Table` object which will accept the bets. It also provides
            access to the `wheel.all_outcomes` structure to pick from.
    """

    def __init__(self, table: Table) -> None:
        """Invokes superclass constructor and and initialise the rng."""
        super().__init__(table)
        self.rng = random.Random()

    def place_bets(self) -> None:
        """Updates the `Table` object with a randomly placed `Bet` instance."""
        random_outcome = self.rng.choice(list(self.table.wheel.all_outcomes.values()))
        current_bet = Bet(1, random_outcome)
        self.table.place_bet(current_bet)
        self.stake -= current_bet.amount


class Player1326(Player):
    """ "A `Player` who follows the 1-3-2-6 betting system. The player has a preferred
    `Outcome` instance. This should be an even money bet. The player also has a
    current betting state that determines the current bet to place, and what next
    state applies when the bet has won or lost.

    Attributes:
        table: The `Table` object which will accept the bets.
        outcome: This is the player's preferred `Outcome` instance, fetched from the
            `Table.Wheel` object.
        state: The current state of the 1-3-2-6 betting system. It will be an instance
            of the `Player1326State` class. This will be one of the four states:
            no wins, one win, two wins or three wins.
    """

    state: "Player1326State"
    outcome: Outcome

    def __init__(self, table: Table) -> None:
        """Invokes the superclass constructor and initialises the state and outcome."""
        super().__init__(table)
        self.outcome = self.table.wheel.get_outcome("Black")
        self.state = Player1326NoWins(self)

    def place_bets(self) -> None:
        """Updates the `Table` with a bet created by the current state. Delegates
        `Bet` creation to the `self.state.current_bet` method.
        """
        current_bet = self.state.current_bet()
        if current_bet.amount > self.stake:
            current_bet.amount = self.stake
        self.table.place_bet(current_bet)
        self.stake -= current_bet.amount

    def win(self, bet: Bet) -> None:
        """Uses the superclass method to update stake with the amount won. Uses
        the current state to transition to the next state.

        Args:
            bet: The `Bet` which won.
        """
        super(Player1326, self).win(bet)
        self.state = self.state.next_won()

    def lose(self, bet: Bet) -> None:
        """Uses the current state to transition to the next state.

        Args:
            bet: The `Bet` which lost.
        """
        self.state = self.state.next_lost()


class Player1326State:
    """Superclass for all of the states in the 1-3-2-6 betting system.

    Attributes:
        player: The `Player1326` player currently in this state. This object will
            be used to provide the `Outcome` object used in creating the `Bet`
            instance.
        next_state_win: The next state to transition to if the bet was a winner.
        bet_amount: The amount bet in this state.
    """

    def __init__(
        self,
        player: Player1326,
        next_state_win: Type["Player1326State"],
        bet_amount: int,
    ) -> None:
        """Initialise class with arguments provided by the subclass state constructors."""
        self.player = player
        self.next_state_win = next_state_win
        self.bet_amount = bet_amount

    def current_bet(self) -> Bet:
        """Constructs a new `Bet` object from the ``player``'s preferred `Outcome`
        instance. Each subclass provides a different multiplier used when creating
        this `Bet` object.

        Returns:
            The `Bet` to be placed when in this state.
        """
        return Bet(self.bet_amount, self.player.outcome)

    def next_won(self) -> "Player1326State":
        """Constructs the new `Player1326State` instance to be used when the bet
        was a winner

        Returns:
            The `Player1326State` to transition to on a winning bet.
        """
        return self.next_state_win(self.player)  # type: ignore

    def next_lost(self) -> "Player1326State":
        """Constructs the new `Player1326State` instance to be used when the bet
        was a loser. This method is the same for each subclass.

        Returns:
            The `Player1326State` to transition to on a losing bet.
        """
        return Player1326NoWins(self.player)


class Player1326NoWins(Player1326State):
    """Defines bet and state transition rules in the 1-3-2-6 betting system
    for when there are no wins.
    """

    def __init__(self, player: Player1326):
        super(Player1326NoWins, self).__init__(player, Player1326OneWin, 1)


class Player1326OneWin(Player1326State):
    """Defines bet and state transition rules in the 1-3-2-6 betting system
    for when there is one win.
    """

    def __init__(self, player: Player1326):
        super(Player1326OneWin, self).__init__(player, Player1326TwoWins, 3)


class Player1326TwoWins(Player1326State):
    """Defines bet and state transition rules in the 1-3-2-6 betting system
    for when there are two wins.
    """

    def __init__(self, player: Player1326):
        super(Player1326TwoWins, self).__init__(player, Player1326ThreeWins, 2)


class Player1326ThreeWins(Player1326State):
    """Defines bet and state transition rules in the 1-3-2-6 betting system
    for when there are three wins.
    """

    def __init__(self, player: Player1326):
        super(Player1326ThreeWins, self).__init__(player, Player1326NoWins, 6)


class PlayerCancellation(Player):
    """A `Player` who uses the cancellation betting system. This player allocates
    their available budget into a sequence of bets that have an accelerating potential
    gain as well as recouping any losses.

    Attributes:
        sequence: This `List` keeps the bet amounts. Wins are removed from this list
            and losses are appended to this list. The current bet is the first value
            plus the last value.
        outcome: The player's preferred `Outcome` instance to bet on.
        table: The `Table` object which will accept the bets.
    """

    sequence: List[int]
    outcome: Outcome

    def __init__(self, table: Table) -> None:
        """Uses the `PlayerCancellation.reset_sequence` method to initialise the
        sequences of numbers used to establish the bet amount. This also picks a
        suitable even money `Outcome`.
        """
        super().__init__(table)
        self.sequence = []
        self.outcome = self.table.wheel.get_outcome("Black")

    def reset(self, duration, stake):
        """Sets `stake`, `rounds_to_go` and `sequence` back to their initial values."""
        super(PlayerCancellation, self).reset(duration, stake)
        self.reset_sequence()

    def reset_sequence(self):
        """Puts the initial sequence of 6 values into the `self.sequence` attribute."""
        self.sequence = [1, 2, 3, 4, 5, 6]

    def place_bets(self) -> None:
        """Creates a bet from the sum of the first and last values of `self.sequence`
        and the preferred outcome.

        Reset the sequence once we have completed the betting strategy and
        `self.sequence` is empty. Stop playing if a bet exceeds `table.limit`.
        """
        if len(self.sequence) > 1:
            current_bet = Bet(self.sequence[0] + self.sequence[-1], self.outcome)
            if current_bet.amount > self.stake:
                current_bet.amount = self.stake
            try:
                self.table.place_bet(current_bet)
            except InvalidBet:
                self.rounds_to_go = 0
                return
            self.stake -= current_bet.amount
        else:
            self.reset_sequence()

    def win(self, bet: Bet) -> None:
        """Uses the superclass method to update the stake with an amount won. It
        then removes the first and last element from `self.sequence`.

        Args:
            bet: The `Bet` which won.
        """
        super(PlayerCancellation, self).win(bet)
        self.sequence = self.sequence[1:-1]

    def lose(self, bet: Bet) -> None:
        """Uses the superclass method to update the stake with an amount lose. It
        then appends the sum of the first and last elements of `self.sequence` to
        the end of `self.sequence`.

        Args:
            bet: The `Bet` which lost.
        """
        super(PlayerCancellation, self).lose(bet)
        self.sequence.append(self.sequence[0] + self.sequence[-1])


class PlayerFibonacci(Player):
    """A `Player` who uses the Fibonacci betting system. This player allocates
    their available budget into a sequence of bets that have an accelerating
    potential gain.

    Attributes:
        recent: The most recent bet amount. Initially set to 1.
        previous: The bet amount previous to the most recent bet. Initially set
            to 0.
        table: The `Table` object which will accept the bets.
    """

    recent: int
    previous: int

    def __init__(self, table: Table) -> None:
        """Initialise the Fibonacci player."""
        super().__init__(table)
        self.recent = 1
        self.previous = 0

    def reset(self, duration: int, stake: int) -> None:
        super(PlayerFibonacci, self).reset(duration, stake)
        self.reset_bet_state()

    def reset_bet_state(self):
        """Reset `recent` and `previous` to their initial state."""
        self.recent, self.previous = 1, 0

    def place_bets(self) -> None:
        """Create and place a `Bet` of a value according to `recent` + `previous`."""
        current_bet = Bet(self.recent, self.table.wheel.get_outcome("Black"))
        if current_bet.amount > self.stake:
            current_bet.amount = self.stake
        try:
            self.table.place_bet(current_bet)
        except InvalidBet:
            self.rounds_to_go = 0
            return
        self.stake -= current_bet.amount

    def win(self, bet: Bet) -> None:
        """Users the superclass method to update the stake with an amount won.
        It also resets the betting system state.

        Args:
            bet: The `Bet` which won.
        """
        super(PlayerFibonacci, self).win(bet)
        self.reset_bet_state()

    def lose(self, bet: Bet) -> None:
        """Updates `recent` and `previous` to their values for the next step in
        the betting strategy.

        Args:
            bet: The `Bet` which lost.
        """
        super(PlayerFibonacci, self).lose(bet)
        next_ = self.recent + self.previous
        self.previous = self.recent
        self.recent = next_


class CrapsGame:
    """Stub for `CrapsGame`. Contains interface used by the `Throw` class
    hierarchy to implement game state changes.

    Attributes:
        current_point: The current point. This will be replaced by a proper state design
        pattern.
    """

    current_point: Optional[int]

    def __init__(self) -> None:
        """Creates this game. A later version will use a constructor to include
        the `Dice` and `CrapsTable` instances."""
        self.current_point = None

    def craps(self) -> None:
        """Resolves all current 1-roll bets.

        If the point is zero, this was a come out roll: Pass Line bets are an
        immediate loss, Don’t Pass Line bets are an immediate win.

        If the point is non-zero, Come Line bets are an immediate loss; Don’t
        Come Line bets are an immediate win.

        The state doesn't change.

        A future version will delegate responsibility to the craps() method of
        a current state object.
        """
        ...

    def natural(self) -> None:
        """A roll of 7 occurred. Resolves all current 1-roll bets.

        If the point is None, this was a come out roll: Pass Line bets are an
        immediate win; Don’t Pass Line bets are an immediate loss.

        If the point is non-None, Come Line bets are an immediate win; Don’t
        Come bets are an immediate loss; the point is also reset to zero
        because the game is over.

        Also, hardways bets are all losses.

        A future version will delegate responsibility to the natural() method
        of a current state object.
        """
        if self.current_point:
            self.current_point = None

    def eleven(self) -> None:
        """Resolves all current 1-roll bets.

        If the point is None, this was a come out roll: Pass Line bets are an
        immediate win; Don’t Pass Line bets are an immediate loss.

        If the point is non-None, Come Line bets are an immediate win; Don’t
        Come bets are an immediate loss; the point is also reset to zero
        because the game is over.

        Also, hardways bets are all losses.

        A future version will delegate responsibility to the natural() method
        of a current state object.
        """
        ...

    def point(self) -> None:
        """Resolves all current 1-roll bets.

        If the point was None, this is a come out roll, and the value of the
        dice establishes the point.

        If the point was non-None and this throw matches the point the game is
        over: Pass Line bets and associated odds bets are winners; Don’t Pass
        bets and associated odds bets are losers; the point is reset to zero.

        Finally, if the point is non-None and this throw does not match the
        point, the state doesn't change. Come point and Don’t come point bets
        may be resolved. Additionally, hardways bets may be resolved.

        A future version will delegate responsibility to the current state’s
        point() method to advance the game state.
        """
        if self.current_point is None:
            self.current_point = "dice roll"  # Set point to value of dice roll.
        elif self.current_point == "dice roll":
            # Win this game and set point off.
            self.current_point = None

    def __str__(self) -> str:
        """TODO: Update when `CrapsGame` has an internal state."""
        return str(self.current_point) if self.current_point else "Point Off"


class RouletteGame:
    """`RouletteGame` manages the sequence of actions that defines the game of Roulette.

    This includes notifying the `Player` object to place bets, spinning the
    `Wheel` object and resolving the `Bet` instances actually present on the
    `Table` object.

    Attributes:
        wheel: The `Wheel` instance which produces random events.
        table: The `Table` instance which holds bets to be resolved.
    """

    def __init__(self, table: Table, wheel: Wheel) -> None:
        self.wheel = wheel
        self.table = table

    def cycle(self, player: Player):
        """Execute a single cycle of play with a given `Player`.

        Args:
            player: The individual `Player` that places bets, receives winnings
            and pays losses.
        """
        if player.playing():
            player.place_bets()
            self.table.validate()
            winning_bin = self.wheel.choose()
            player.winners(winning_bin.outcomes)
            for bet in self.table:
                if bet.outcome in winning_bin:
                    player.win(bet)
                else:
                    player.lose(bet)
            self.table.clear()
            player.rounds_to_go -= 1


class Simulator:
    """`Simulator` exercises the Roulette simulation with a given `Player` placing
    bets. It reports raw statistics on a number of sessions of play.

    Attributes:
        init_duration: The duration (`Player.rounds_to_go`) value to use when
            initialising a `Player` instance for a session.
        init_stake: The stake value to use when initialising a `Player` instance
            for a session. This is a count of the initial number of the bets
            placeable at the table's minimum bet value. I.e set to 100 on a table
            with a minimum bet of £10 would equate to a £1000 stake.
        samples: The number of game session cycles to simulate.
        durations: A `list` of lengths of time the `Player` object remained in
            the game. Each session produces a duration metric.
        maxima: A `list` of maximum stakes for the `Player` object from each game
            session. The highest stake value reached for each session.
        end_stakes: A `list` of the player's stake at the end of their session.
        player: The `Player` instance. This encapsulates the betting strategy we
            are simulating.
        game: The casino game we are simulating. This is an instance of the `Game`
            class, which embodies the various rules, the `Table` object and the
            `Wheel` instance.
    """

    init_duration: int
    init_stake: int
    samples: int
    durations: "IntegerStatistics"
    maxima: "IntegerStatistics"
    end_stakes: "IntegerStatistics"

    def __init__(self, game: RouletteGame, player: Player) -> None:
        self.init_duration = 250
        self.init_stake = 100
        self.samples = 50
        self.durations = IntegerStatistics()
        self.maxima = IntegerStatistics()
        self.end_stakes = IntegerStatistics()
        self.player = player
        self.game = game

    def session(self) -> List[int]:
        """Executes a single game session.

        The `Player` initial `stake` and `cycles_to_go` are set/reset and a full
        game session is completed accordingly by calling the `game.cycle` method
        until `player.playing()` returns False. The players `stake` after each
        round of play is recorded.

        Returns:
            A list of individual `Player.stake` values after each cycle.
        """
        self.player.reset(self.init_duration, self.init_stake)
        stake_values = []
        while self.player.playing():
            self.game.cycle(self.player)
            stake_values.append(self.player.stake)

        return stake_values

    def gather(self) -> None:
        """Executes the number of games in `samples` and records statistics.

        Each game session returns a `list` of stake values which are used to
        calculate the duration and maxima metrics for that session.
        """
        for _ in range(self.samples):
            stake_values = self.session()
            self.durations.append(len(stake_values))
            self.maxima.append(max(stake_values))
            self.end_stakes.append(stake_values[-1])


class IntegerStatistics(typing.List[int]):
    """Computes several simple descriptive statistics of `int` values in a `list`.

    This extends `list` with some additional methods.
    """

    def mean(self) -> float:
        """Computes the mean of the `List` of values."""
        return round(sum(self) / len(self), 2)

    def stdev(self) -> float:
        """Computes the standard deviation of the `List` of values."""
        m = self.mean()
        return round(math.sqrt(sum((x - m) ** 2 for x in self) / (len(self) - 1)), 2)


class BulkSimulator:
    """Executes a `Simulator` instance for each `Player` subclass and writes metrics
    to a CSV file.

    Attributes:
        game: The casino game we are simulating. This is an instance of the `Game`
            class, which embodies the various rules, the `Table` object and the
            `Wheel` instance.
        players: A `List` of all `Player` subclasses.
        player_stats: A `list` of `dict`'s containing the stats for each player's
            `Simulator` run.
    """

    players: List[Type[Player]]
    player_stats: List[Dict]

    def __init__(self, game: RouletteGame) -> None:
        """Initialise `BulkSimulator` with the `game` we are simulating and gather
        all the player objects into self.players."""
        self.game = game
        self.players = self.get_all_players()
        self.player_stats = []

    def get_all_players(self) -> List[Type[Player]]:
        """Recursively gathers the subclasses of ``cls``.

        Returns:
            A `list` containing each subclass object of ``cls`` and any subclasses
                of their subclasses.
        """
        all_players = set()
        for sub_cls in Player.__subclasses__():
            all_players.add(sub_cls)
            for sub_cls_sub in sub_cls.__subclasses__():
                all_players.add(sub_cls_sub)

        # Ensure players are always in the same order for csv row order
        #  consistency and ease of testing.
        all_players_list = list(all_players)
        all_players_list.sort(key=lambda x: x.__name__)
        return all_players_list

    def gather_all(self) -> None:
        """Behaves similarly to `Simulator.gather` but gathers statistics for every
        `Player` subclass and adds them as a `dict` to `self.player_stats`.
        """
        for player in self.players:
            p = player(self.game.table)
            p_sim = Simulator(self.game, p)
            p_sim.gather()
            self.player_stats.append(
                {
                    "player": p.__class__.__name__,
                    "duration_mean": p_sim.durations.mean(),
                    "duration_stdev": p_sim.durations.stdev(),
                    "maxima_mean": p_sim.maxima.mean(),
                    "maxima_stdev": p_sim.maxima.stdev(),
                    "end_stake_mean": p_sim.end_stakes.mean(),
                    "end_stake_stdev": p_sim.end_stakes.stdev(),
                }
            )

    def save_to_csv(self, file_path) -> None:
        """Saves stats gathered with `self.gather_all` to a CSV file located in
        the current working directory.

        Args:
            file_path: The path to save the csv. E.g. "stats.csv" or
                "C:\\Users\\Me\\stats.csv" or "./data/stats.csv"
        """
        with open(file_path, "w", newline="") as csv_file:
            fieldnames = [field for field in self.player_stats[0].keys()]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.player_stats)


def print_sim_results(sim: Simulator) -> None:
    """Print the results from a single `Simulator` instance after it is populated
    with statistics from running its `gather` method.

    Args:
        sim: A `Simulator` instance which has gathered statistics to be printed.
    """

    if not sim.durations:
        sim.gather()

    print(f"{'n':5s}{'Duration':>15s}{'Maxima':>15s}{'End Stake':>15s}\n{'-'*50}")
    for n, duration, maxima, end in zip(
        range(len(sim.maxima)), sim.durations, sim.maxima, sim.end_stakes
    ):
        print(f"{n+1:<5d}{duration:>15d}{maxima:>15d}{end:>15d}")

    print(
        f"{'-'*50}\n{'Mean':<5s}"
        f"{sim.durations.mean():>15.2f}"
        f"{sim.maxima.mean():>15.2f}"
        f"{sim.end_stakes.mean():>15.2f}"
        f"\n{'Stdev':<5s}"
        f"{sim.durations.stdev():>15.2f}"
        f"{sim.maxima.stdev():>15.2f}"
        f"{sim.end_stakes.stdev():>15.2f}"
    )


def main():
    table = Table()
    game = RouletteGame(table, table.wheel)
    # # To run a simulation for just one player and print the results:
    player = PlayerFibonacci(table)
    sim = Simulator(game, player)
    sim.gather()
    print_sim_results(sim)
    # bulk_sim = BulkSimulator(game)
    # bulk_sim.gather_all()
    # bulk_sim.save_to_csv("sim_stats.csv")


if __name__ == "__main__":
    main()
