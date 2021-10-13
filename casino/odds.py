"""Collection of constants of odds for each type of bet where all
bets pay x:1.

E.g. A split bet pays at 17:1.
"""

# Roulette
STRAIGHT: int = 35  # A single number.
SPLIT: int = 17  # Adjacent pair of numbers.
STREET: int = 11  # Three numbers in a single row.
CORNER: int = 8  # Square of four numbers.
FIVE: int = 6  # 0, 00, 1, 2 and 3.
LINE: int = 5  # Two adjacent street bets.
DOZEN: int = 2  # 12-number ranges (1-12, 13-24, 25-36).
COLUMN: int = 2  # 12-number columns.
EVEN: int = 1  # Even, odd, high, low, red, black.

# Craps
PASS_COME: int = 1
DONT_PASS_COME: int = 1
PROP_2: int = 30
PROP_3: int = 15
PROP_11: int = 15
PROP_12: int = 30
ANY_7: int = 4
ANY_CRAPS: int = 7
HORN: int = 3  # Variable odds; dependant on event_id
FIELD: int = 1  # Variable odds; dependant on event_id
HARD_6_8: int = 9
HARD_4_10: int = 7
