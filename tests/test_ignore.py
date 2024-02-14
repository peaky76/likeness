import operator
from typing import Callable, ClassVar

from likeness import LikenessMixin, ignore


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
