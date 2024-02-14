import operator
from typing import Callable, ClassVar

import pytest

from likeness import LikenessMixin


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
