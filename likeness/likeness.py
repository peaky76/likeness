from .likeness_mixin import LikenessMixin


def likeness(a: LikenessMixin, b: LikenessMixin) -> float:
    return a.like(b)
