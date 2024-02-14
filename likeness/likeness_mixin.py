from typing import Callable, ClassVar, Self

from numpy import array, prod


class LikenessMixin:
    _likeness_functions: ClassVar[dict[str, Callable]] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # forwards all unused arguments

    def like(self, other: Self) -> float:
        likeness_base = float(bool(len(self._likeness_functions)) or self == other)

        factors = []
        for attribute, function in self._likeness_functions.items():
            try:
                a = getattr(self, attribute)
                b = getattr(other, attribute)
                factors.append(function(a, b))
            except Exception:  # noqa: PERF203
                raise ValueError(
                    f"Unable to calculate likeness: {attribute} comparison failed"
                )

        return prod(array([likeness_base, *factors]))
