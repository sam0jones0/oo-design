"""TODO"""

import pytest

from casino.main import IntegerStatistics


def test_integer_statistics():
    test_data = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7]
    int_stat = IntegerStatistics(test_data)
    int_stat.append(5)

    assert sum(int_stat) == 99
    assert len(int_stat) == 11
    assert int_stat.mean() == 9.0
    assert round(int_stat.stdev(), 3) == 3.32
