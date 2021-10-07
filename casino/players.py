"""TODO"""

from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import FrozenSet, Type, List, Optional

import casino.main
import casino.odds


class Player(ABC):
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

    def __init__(self, table: casino.main.Table) -> None:
        """Constructs the `Player` instance with a specific `Table` object for
        placing `Bet` instances.
        """
        self.table = table
        self.stake = 0
        self.rounds_to_go = 0

    @abstractmethod
    def place_bets(self) -> None:
        """Must be overridden in subclass as each `Player` will have different
        betting strategy.
        """
        pass

    def reset(self, duration: int, stake: int) -> None:
        """Sets `stake` and `rounds_to_go` according to the values passed by the
        overall simulation control. Called before the start of a new session.

        Args:
            duration: The number of `rounds_to_go` for the next session.
            stake: The initial stake to begin the next session with.
        """
        self.rounds_to_go = duration
        self.stake = stake

    def playing(self) -> bool:
        """Returns `True` while the player is still active."""
        if self.rounds_to_go > 0 and self.stake > 0:
            return True
        else:
            return False

    def win(self, bet: casino.main.Bet) -> None:
        """Notification from the `Game` object that the `Bet` instance was a
        winner. Increases `Player.stake` accordingly.

        Args:
              bet: The `Bet` which won.
        """
        self.stake += bet.win_amount()

    def lose(self, bet: casino.main.Bet) -> None:
        """Notification from the `Game` object that the `Bet` instance was a loser.

        Does nothing by default, some subclassed players will take particular actions
        on losses.
        """
        pass

    def winners(self, outcomes: FrozenSet[casino.main.Outcome]) -> None:
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

    black: casino.main.Outcome

    def __init__(self, table: casino.main.Table) -> None:
        """Constructs the `Player` instance with a specific `Table` and `Wheel
        for creating and resolving bets. Also creates the 'black' `Outcome` for
        use in creating bets.
        """
        super().__init__(table)
        self.black = table.wheel.get_outcome("black")

    def place_bets(self) -> None:
        """Create and place one `Bet` on the 'Black' `Outcome` instance."""
        current_bet = casino.main.Bet(
            1, self.black, self
        )  # Stake will be >= 1 if self.playing()
        self.table.place_bet(current_bet)


class Martingale(Player):
    """`Martingale` is a `Player` subclass who places bets in Roulette. This player doubles
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

    def __init__(self, table: casino.main.Table) -> None:
        super().__init__(table)
        self.bet_multiple = 1
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
        current_bet = casino.main.Bet(
            bet_amount, self.table.wheel.get_outcome("black"), self
        )
        try:
            self.table.place_bet(current_bet)
        except casino.main.InvalidBet:
            self.reset(self.rounds_to_go, self.stake)
            self.place_bets()
            return

    def win(self, bet: casino.main.Bet) -> None:
        """Uses the superclass `Player.win()` method to update the stake with an
        amount won. Then resets `loss_count` to zero and resets `bet_multiple`
        to 1.

        Args:
            bet: The winning bet.
        """
        super(Martingale, self).win(bet)
        self.loss_count = 0
        self.bet_multiple = 1

    def lose(self, bet: casino.main.Bet) -> None:
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
    """This is a `Player` subclass who places bets in roulette. They wait until
    the wheel has spun red seven times in a row before betting on black.

    Attributes:
        table: The `Table` that is used to place individual `Bet` instances.
        red_count: The number of reds yet to go. Inits to 7, and is reset to 7 on
            each non-red outcome, and decrements by 1 on each red outcome.
    """

    def __init__(self, table: casino.main.Table) -> None:
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

    def winners(self, outcomes: FrozenSet[casino.main.Outcome]) -> None:
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
    """A `Player` subclass who places bets in roulette. This player makes random bets
    around the layout.

    Attributes:
        rng: A random number generator for selecting outcomes to bet on.
        table: The `Table` object which will accept the bets. It also provides
            access to the `wheel.all_outcomes` structure to pick from.
    """

    def __init__(self, table: casino.main.Table) -> None:
        """Invokes superclass constructor and and initialise the rng."""
        super().__init__(table)
        self.rng = random.Random()

    def place_bets(self) -> None:
        """Updates the `Table` object with a randomly placed `Bet` instance."""
        random_outcome = self.rng.choice(list(self.table.wheel.all_outcomes.values()))
        current_bet = casino.main.Bet(1, random_outcome, self)
        self.table.place_bet(current_bet)


class Player1326(Player):
    """ "A `Player` subclass who follows the 1-3-2-6 betting system. The player has a preferred
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
    outcome: casino.main.Outcome

    def __init__(self, table: casino.main.Table) -> None:
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

    def win(self, bet: casino.main.Bet) -> None:
        """Uses the superclass method to update stake with the amount won. Uses
        the current state to transition to the next state.

        Args:
            bet: The `Bet` which won.
        """
        super(Player1326, self).win(bet)
        self.state = self.state.next_won()

    def lose(self, bet: casino.main.Bet) -> None:
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

    def current_bet(self) -> casino.main.Bet:
        """Constructs a new `Bet` object from the ``player``'s preferred `Outcome`
        instance. Each subclass provides a different multiplier used when creating
        this `Bet` object.

        Returns:
            The `Bet` to be placed when in this state.
        """
        return casino.main.Bet(self.bet_amount, self.player.outcome, self.player)

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
    """A `Player` subclass who uses the cancellation betting system. This player allocates
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
    outcome: casino.main.Outcome

    def __init__(self, table: casino.main.Table) -> None:
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
            current_bet = casino.main.Bet(
                self.sequence[0] + self.sequence[-1], self.outcome, self
            )
            if current_bet.amount > self.stake:
                current_bet.amount = self.stake
            try:
                self.table.place_bet(current_bet)
            except casino.main.InvalidBet:
                self.rounds_to_go = 0
                return
        else:
            self.reset_sequence()

    def win(self, bet: casino.main.Bet) -> None:
        """Uses the superclass method to update the stake with an amount won. It
        then removes the first and last element from `self.sequence`.

        Args:
            bet: The `Bet` which won.
        """
        super(PlayerCancellation, self).win(bet)
        self.sequence = self.sequence[1:-1]

    def lose(self, bet: casino.main.Bet) -> None:
        """Uses the superclass method to update the stake with an amount lose. It
        then appends the sum of the first and last elements of `self.sequence` to
        the end of `self.sequence`.

        Args:
            bet: The `Bet` which lost.
        """
        super(PlayerCancellation, self).lose(bet)
        self.sequence.append(self.sequence[0] + self.sequence[-1])


class PlayerFibonacci(Player):
    """A `Player` subclass who uses the Fibonacci betting system. This player allocates
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

    def __init__(self, table: casino.main.Table) -> None:
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
        current_bet = casino.main.Bet(
            self.recent, self.table.wheel.get_outcome("Black"), self
        )
        if current_bet.amount > self.stake:
            current_bet.amount = self.stake
        try:
            self.table.place_bet(current_bet)
        except casino.main.InvalidBet:
            self.rounds_to_go = 0
            return

    def win(self, bet: casino.main.Bet) -> None:
        """Users the superclass method to update the stake with an amount won.
        It also resets the betting system state.

        Args:
            bet: The `Bet` which won.
        """
        super(PlayerFibonacci, self).win(bet)
        self.reset_bet_state()

    def lose(self, bet: casino.main.Bet) -> None:
        """Updates `recent` and `previous` to their values for the next step in
        the betting strategy.

        Args:
            bet: The `Bet` which lost.
        """
        super(PlayerFibonacci, self).lose(bet)
        next_ = self.recent + self.previous
        self.previous = self.recent
        self.recent = next_


class CrapsPlayer(Player):
    """A `Player` for the game of Craps. This player constructs a `Bet` instance
    based on the `Outcome` instance named 'Pass Line'. This is a very persistent
    player.

    # TODO: This is a stub class to enable CrapsGame to be written. Needs expanding.

    Attributes:
        pass_line: This is the `Outcome` on which this player focuses their betting.
            It will be an instance of the 'Pass Line' `Outcome` with 1:1 odds.
        working_bet: This is the current 'Pass Line' `Bet`. Each time a bet is resolved
            this is reset to `None`, ensuring only one bet is working at a time.
        table: The `Table` which collects all bets.
    """

    pass_line: casino.main.Outcome
    working_bet: Optional[casino.main.Bet]
    table: casino.main.CrapsTable

    def __init__(self, table: casino.main.CrapsTable) -> None:
        """Constructs the `CrapsPlayer` instance with a specific table for placing
        bets.
        """
        super(CrapsPlayer, self).__init__(table)
        self.pass_line = casino.main.Outcome("Pass Line", casino.odds.PASS_COME)
        self.working_bet = None

    def place_bets(self) -> None:
        """Places a new 'Pass Line' `Bet` if there is no current working bet."""
        if self.working_bet is None:
            bet = casino.main.Bet(1, self.pass_line, self)
            self.table.place_bet(bet)
            self.working_bet = bet

    def win(self, bet: casino.main.Bet) -> None:
        self.working_bet = None
        super(CrapsPlayer, self).win(bet)

    def lose(self, bet: casino.main.Bet) -> None:
        self.working_bet = None
        super(CrapsPlayer, self).lose(bet)
