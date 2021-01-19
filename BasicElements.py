from AnimationElement import AnimationElement
from myMaths import Vec2D

import math


class TextElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D,
                 axes, s_text: str, **kwargs):
        AnimationElement.__init__(self, start, duration, position)

        self._axes = axes
        self._textArgs = kwargs
        self._text = s_text

    def _instantiate(self):
        self._textElem = self._axes.text(self._position.x, self._position.y, self._text, self._textArgs)

    def _update(self, progress):
        self._textElem.set_position((self._position.x + 10 * math.sin(4 * math.pi * progress), self._position.y))

    def _cleanup(self):
        self._textElem.set_visible(False)
        return 0
