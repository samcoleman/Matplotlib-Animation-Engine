from myMaths import Vec2D
from mpl_toolkits.axes_grid1.inset_locator import (InsetPosition)
import matplotlib.pyplot as plt

# Animation Element, start time and end time
class AnimationElement:
    def __init__(self, main_axes, start: float, end: float, position: Vec2D):
        self._exists = False

        self._start = start
        self._end = end
        self._position = position

        self._main_axes = main_axes

    def update(self, frame, fps):
        if self._start * fps <= frame < self._end * fps:
            # Minus one start/end zero indexed so last frame object is not shown
            progress = (frame - (self._start * fps)) / (((self._end - self._start) * fps) - 1)

            try:
                return self._update_element(progress)
            except Exception as detail:
                print("Error:", detail)
            return None
        elif frame == self._end * fps:
            try:
                return self._cleanup_element()
            except Exception as detail:
                print("Error:", detail)
            return None

    def _update_element(self, progress):
        raise Exception("Element Update Not Implemented")

    def _cleanup_element(self):
        raise Exception("Element Cleanup Not Implemented")


class TextElement(AnimationElement):
    def __init__(self, main_axes,start: float, end: float, position: Vec2D,
                 s_text: str, **kwargs):

        AnimationElement.__init__(self, main_axes, start, end, position)

        self._textArgs = kwargs
        self._text = s_text

    def _update_element(self, progress):
        self._textElem = self._main_axes.text(self._position.x, self._position.y, self._text, self._textArgs)

    def _cleanup_element(self):
        self._textElem.set_visible(False)
        return 0


class FigElement(AnimationElement):
    def __init__(self, main_axes, start: float, end: float, position: Vec2D,
                 fig):
        AnimationElement.__init__(self, main_axes, start, end, position)

        self._fig = fig
        self._fig.axes = None

    def _update_element(self, progress):
        if self._fig.axes is None:
            self._fig.axes = plt.axes([0, 0, 1, 1])
            ip = InsetPosition(self._main_axes, [0.25, 0.25, .5, .5])
            self._fig.axes.set_axes_locator(ip)

        self._fig.plot(progress)
        return 0

    def _cleanup_element(self):

        return 0
