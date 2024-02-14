import operator
from typing import Callable, ClassVar

import pytest

from likeness.likeness_mixin import LikenessMixin, discount, ignore, likeness


def test_likeness_mixin_default_when_objects_different():
    class DummyClass(LikenessMixin):
        pass

    dummy_1 = DummyClass()
    dummy_2 = DummyClass()
    assert dummy_1.like(dummy_2) == 0


def test_likeness_mixin_default_when_objects_same():
    class DummyClass(LikenessMixin):
        pass

    single_object = DummyClass()
    dummy_1 = single_object
    dummy_2 = single_object
    assert dummy_1.like(dummy_2) == 1


def test_likeness_mixin_with_functions():
    class DummyClass(LikenessMixin):
        _likeness_functions: ClassVar[dict[str, Callable]] = {
            "foo": operator.mul,
            "bar": lambda a, b: a / float(b),
        }

        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    dummy_1 = DummyClass(1, 1)
    dummy_2 = DummyClass(0.5, 2)

    assert dummy_1.like(dummy_2) == 0.25


def test_likeness_mixin_with_functions_raises_error_if_function_fails():
    class DummyClass(LikenessMixin):
        _likeness_functions: ClassVar[dict[str, Callable]] = {
            "foo": operator.mul,
            "bar": operator.truediv,
        }

        def __init__(self, foo, bar=None):
            self.foo = foo
            self.bar = bar

    dummy_1 = DummyClass(1, 1)
    dummy_2 = DummyClass(0.5)

    with pytest.raises(ValueError, match="Unable to calculate likeness"):
        dummy_1.like(dummy_2)


def test_discount_when_fn_returns_float_between_0_and_1():
    assert discount(0.5) == 0.5


def test_discount_when_fn_returns_float_greater_than_1():
    assert discount(1.1) == 0


def test_discount_errors_when_fn_returns_float_less_than_0():
    with pytest.raises(ValueError, match="Discount function must return a value below 1"):
        discount(-0.1)


def test_ignore():
    class DummyClass(LikenessMixin):
        _likeness_functions: ClassVar[dict[str, Callable]] = {
            "foo": operator.mul,
            "bar": lambda a, b: a / float(b),
        }

        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    dummy_1 = DummyClass(1, 1)
    dummy_2 = DummyClass(0.5, 2)

    assert ignore(dummy_1, dummy_2) == 1


def test_likeness():
    class DummyClass(LikenessMixin):
        _likeness_functions: ClassVar[dict[str, Callable]] = {
            "foo": operator.mul,
            "bar": lambda a, b: a / float(b),
        }

        def __init__(self, foo, bar):
            self.foo = foo
            self.bar = bar

    dummy_1 = DummyClass(1, 1)
    dummy_2 = DummyClass(0.5, 2)

    assert likeness(dummy_1, dummy_2) == 0.25