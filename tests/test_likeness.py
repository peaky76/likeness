import operator
from collections.abc import Callable
from typing import ClassVar

from likeness import LikenessMixin, likeness


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
