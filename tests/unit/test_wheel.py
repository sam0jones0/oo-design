"""
TODO
"""

import pytest

from roulette.roulette import Wheel


@pytest.mark.usefixtures("do_not_build_bins")
class TestWheel:
    def test_add(self, mock_outcomes):
        o1, o2, o3 = mock_outcomes
        wheel = Wheel()
        wheel.add_outcomes(8, [o1])
        wheel.add_outcomes(8, [o2, o3])

        assert len(wheel.all_outcomes) == 3

    def test_choose(self, seeded_wheel, mock_outcomes):
        o1, o2, o3 = mock_outcomes
        wheel = seeded_wheel
        wheel.add_outcomes(8, mock_outcomes)
        # First randint(0, 37) of seeded_wheel will return 8.
        random_bin = wheel.choose()

        assert o1 in random_bin
        assert o2 in random_bin
        assert o3 in random_bin
        assert o1 in wheel.get_bin(8)
        assert o2 in wheel.get_bin(8)
        assert o3 in wheel.get_bin(8)

    def test_get(self, wheel_with_outcomes, mock_outcomes):
        o1, o2, o3 = mock_outcomes
        wheel = wheel_with_outcomes

        assert wheel.get_outcome(o1.name) is o1
        assert wheel.get_outcome(o2.name) is o2
        assert wheel.get_outcome(o3.name) is o3

        with pytest.raises(KeyError) as exc_info:
            wheel.get_outcome("does_not_exist")
        exception_msg = exc_info.value.args[0]
        assert exception_msg == "No Outcome with name: does_not_exist"
