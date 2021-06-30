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
        odds: The payout odds of this outcome. Most odds are stated as 1:1 or
            17:1, we only keep the numerator (17) and assume the denominator is 1.
    """

    def __init__(self, name: str, odds: int) -> None:
        """Sets the instance `name` and `odds` from the parameter `name` and
        `odds`.
        """
        self.name = name
        self.odds = odds

    def win_amount(self, amount: int) -> int:
        """Multiplies this `Outcome`'s odds by the given ``amount`` and returns
        the product.

        Args:
            amount: The amount being bet.

        Returns:
            The amount in winnings excluding the initial bet.
        """
        return self.odds * amount

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
        return f"{self.name} {self.odds}:1"

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

    def __init__(self, rng: Random = None) -> None:
        """Creates a new wheel with 38 empty `Bin` instances, a new random number
         generator instance and a dict to store all possible outcomes.
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
        self.all_outcomes = dict()

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
        for n in range(1, 37):
            outcome = Outcome(f"Number {n}", odds.STRAIGHT)
            self.temp_bins[n].append(outcome)
        self.temp_bins[0].append(Outcome("Number 0", odds.STRAIGHT))
        self.temp_bins[37].append(Outcome("Number 00", odds.STRAIGHT))

    def gen_split_bets(self) -> None:
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
        for row in range(0, 12):
            n = row * 3 + 1
            outcome = Outcome(f"{n}-{n+1}-{n+2} Street", odds.STREET)
            self.temp_bins[n].append(outcome)
            self.temp_bins[n + 1].append(outcome)
            self.temp_bins[n + 2].append(outcome)

    def gen_corner_bets(self) -> None:
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
        for dozen in range(0, 3):
            outcome = Outcome(f"Dozen {dozen+1}", odds.DOZEN)
            for n in range(0, 12):
                self.temp_bins[dozen * 12 + n + 1].append(outcome)

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
        outcome = Outcome("Five", odds.FIVE)
        for n in [0, 37, 1, 2, 3]:
            self.temp_bins[n].append(outcome)


class Bet:
    """A `Bet` on a specific `Outcome`.

    Maintains an association between an amount wagered, an `Outcome` object, and
    the specific `Player` who made the `Bet`.

    TODO: We can’t allow a player to bet more than their stake; therefore, we
        should deduct the payment as the Bet instance is created. A consequence
        of this is a change to our definition of the Bet class. We don’t need to
        compute the amount that is lost. We’re not going to deduct the money
        when the bet resolved, we’re going to deduct the money from the Player
        object’s stake as part of creating the Bet instance.

    TODO: Associate with the specific `Player` making the `Bet`.

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

    def lose_amount(self) -> int:
        """Returns the amount lost on this `Bet`."""
        return self.amount

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
        minimum: This is the table minimum. Each individual bet from a `Player`
            object must be greater than this limit.
        bets: This is a list of the `Bet` instances currently active. These will
            result in either wins or losses to the `Player` object.
        bets_total: A running total of all `Bet`'s amounts in play.
    """

    bets: List[Bet]
    limit: int
    minimum: int
    bets_total: int

    def __init__(self, *bets: Bet) -> None:
        """Creates an empty list of bets."""
        if bets is None:
            self.bets = []
        else:
            self.bets = list(bets)

        self.limit = 300
        self.minimum = 10
        self.bets_total = 0

    def place_bet(self, bet: Bet) -> None:
        """Adds this ``bet`` to the list of active `bets` after checking if placing
        this bet does not violate the table minimum bet/limit rules.

        Args:
            bet: A `Bet` instances to be added to the table.

        Raises:
            InvalidBet: Placing this ``bet`` breaks the table minimum/limit rules.
        """
        if (
            self.minimum <= bet.amount <= self.limit
            and self.bets_total + bet.amount <= self.limit
        ):
            self.bets.append(bet)
            self.bets_total += bet.amount
        else:
            raise InvalidBet("Placing this bet violates table min/limit rules.")

    def is_valid(self) -> bool:
        """Confirms the table-limit rules have been adhered to such that each
        bet is at least `self.minimum` and the sum of all bets is no greater
        than `self.limit`.

        Returns:
            True, if `Table` state is valid.

        Raises:
            InvalidBet: The bets don't pass the table minimum/limit rules.
        """
        total_amount = 0
        for bet in self.bets:
            total_amount += bet.amount
            if not (
                self.minimum <= bet.amount <= self.limit and total_amount <= self.limit
            ):
                raise InvalidBet("Active bets violate the table min/limit rules.")
        return True

    def clear(self) -> None:
        """Clears the table of all `Bet` instances, to be called once `Game` has resolved
        all `Bet`'s."""
        self.bets = []
        self.bets_total = 0

    def __iter__(self) -> Iterator[Bet]:
        """Returns an iterator over the available `Bet` instances."""
        # Note that we need to be able remove bets from the table. Consequently,
        # we have to update the list, which requires that we create a copy of the list.
        return iter(self.bets[:])

    def __str__(self) -> str:
        return ", ".join(str(bet) for bet in self.bets)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(repr(bet) for bet in self.bets)})"


class Passenger57:
    """Temporary `Player`. Constructs a `Bet` instance based on the `Outcome`
    object named 'Black'.

    Attributes:
        table: The `Table` that is used to place individual `Bet` instances.
        wheel: The `Wheel` instance which defines all `Outcome` instances.
        black: The `Outcome` on which this player focuses their betting.
    """

    def __init__(self, table: Table, wheel: Wheel) -> None:
        """Constructs the `Player` instance with a specific `Table` and `Wheel
        for creating and resolving bets. Also creates the 'black' `Outcome` for
        use in creating bets.
        """
        self.table = table
        self.wheel = wheel
        self.black = wheel.get_outcome("black")

    def place_bets(self) -> None:
        """Create an place a `Bet` on the 'Black' `Outcome` instance."""
        self.table.place_bet(Bet(10, self.black))
        # player.pot -= ~bet.amount~

    def win(self, bet: Bet) -> None:
        """Notification from the `Game` object that the `Bet` instance was a winner."""
        # player.pot += bet.win_amount()
        ...

    def lose(self, bet: Bet) -> None:
        """Notification from the `Game` object that the `Bet` instances was a loser."""
        ...


class Game:
    """`Game` manages the sequence of actions that defines the game of Roulette.

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

    def cycle(self, player: Passenger57):  # TODO: `Player` type hint missing/wrong.
        """Execute a single cycle of play with a given `Player`.

        Args:
            player: The individual `Player` that places bets, receives winnings
            and pays losses.
        """
        player.place_bets()
        winning_bin = self.wheel.choose()
        for bet in self.table:
            if bet.outcome in winning_bin:
                player.win(bet)
            else:
                player.lose(bet)
        self.table.clear()


if __name__ == "__main__":
    w = Wheel()
    builder = BinBuilder()
    builder.build_bins(w)
    for i in range(10):
        print("hi")
