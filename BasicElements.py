from AnimationElement import AnimationElement
from myMaths import Vec2D

from Transform import *

import math


class TextElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D,
                 axes, s_text: str, s_size, s: Sequence = None, **kwargs):
        AnimationElement.__init__(self, start, duration, position)

        self._axes = axes
        self._textArgs = kwargs
        self._text = s_text
        self._size = s_size

        self.s = s

    def _instantiate(self):
        self._textElem = self._axes.text(self._position.x, self._position.y, self._text,
                                         self._textArgs, fontsize=self._size)

        self._textTransform = TextTransform(self.s, self._textElem, self._position, 0, self._size)

    def _update(self, p):
        self._position, self._rotation, self._size = self._textTransform.update(p)

    def _cleanup(self):
        self._textElem.set_visible(False)
        return 0
