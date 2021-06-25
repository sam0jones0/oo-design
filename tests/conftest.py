"""TODO"""

import pytest


class MockWheel:
    """Mock of `Wheel` class."""
    @staticmethod
    def add_outcomes(*args, **kwargs):
        return None


@pytest.fixture
def mock_wheel(monkeypatch):
    """Wheel.add_outcomes() mocked to not add outcomes to bins."""
    return MockWheel
