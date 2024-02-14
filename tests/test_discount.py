import pytest

from likeness import discount


def test_discount_when_fn_returns_float_between_0_and_1():
    assert discount(0.5) == 0.5


def test_discount_when_fn_returns_float_greater_than_1():
    assert discount(1.1) == 0


def test_discount_errors_when_fn_returns_float_less_than_0():
    with pytest.raises(
        ValueError, match="Discount function must return a value below 1"
    ):
        discount(-0.1)
