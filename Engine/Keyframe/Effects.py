from Engine.MathsHelpers import Vec2D, Vec3D
from Engine.Keyframe.Keyframe import KeyframeObject
from typing import Union

from matplotlib.text import Text


class Alpha(KeyframeObject):
    def __init__(self, alpha: float):
        super(Alpha, self).__init__()
        self._i_value: Union[None, float] = None
        self._f_value = alpha

    def reset(self) -> None:
        self._handle.set_alpha(self._i_value)

    def _set_start(self) -> None:
        if self._handle.get_alpha() is None:
            self._handle.set_alpha(1.)
        self._i_value = self._handle.get_alpha()

    def _update(self, adj_progress: float, duration: float) -> None:
        self._handle.set_alpha(self._interp(adj_progress))


class Typewrite(KeyframeObject):
    def __init__(self):
        super(Typewrite, self).__init__()

    def _set_start(self) -> None:
        if isinstance(self._handle, Text):
            self._i_value = self._handle.get_text()

    def _update(self, adj_progress: float, duration: float) -> None:
        if isinstance(self._handle, Text):
            pos = int(adj_progress*len(self._i_value))
            self._handle.set_text(self._i_value[:pos])



