from myMaths import Vec2D
import math
from Figures import FigureObj



# Animation Element, start time and end time
class AnimationElement:
    def __init__(self, main_axes, start: float, duration: float, position: Vec2D):
        self._instantiated = False

        self._start = start
        self._end = start + duration
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
    def __init__(self, main_axes, start: float, duration: float, position: Vec2D,
                 s_text: str, **kwargs):
        AnimationElement.__init__(self, main_axes, start, duration, position)

        self._textArgs = kwargs
        self._text = s_text

    def _update_element(self, progress):
        if not self._instantiated:
            self._instantiated = True
            self._textElem = self._main_axes.text(self._position.x, self._position.y,
                                                  self._text, self._textArgs)
        self._textElem.set_position((self._position.x + 10 * math.sin(4 * math.pi * progress), self._position.y))

    def _cleanup_element(self):
        self._textElem.set_visible(False)
        return 0


class FigElement(AnimationElement):
    def __init__(self, main_axes, start: float, duration: float, position: Vec2D,
                 figObj: FigureObj):
        AnimationElement.__init__(self, main_axes, start, duration, position)

        self._figObj = figObj

    def _update_element(self, progress):
        if not self._instantiated:
            self._instantiated = True
            self._figObj.plot()

        self._figObj.update(progress)
        return 0

    def _cleanup_element(self):
        self._figObj.cleanup()
        return 0
