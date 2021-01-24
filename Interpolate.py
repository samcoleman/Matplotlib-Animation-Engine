from myMaths import Vec2D, Vec3D
from typing import Union


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Interpolate:
    def __init__(self, end: Union[float, Vec2D, Vec3D], fn=lambda y: y):
        self._start = 1
        self._end = end
        self._fn = fn

    def set_start(self, start: Union[float, Vec2D, Vec3D]):
        self._start = start

    def interp(self, p):
        return self._start + (self._end - self._start) * clamp(self._fn(p), 0, 1)
