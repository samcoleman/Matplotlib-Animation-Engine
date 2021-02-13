from Engine.Elements.AnimationElement import AnimationElement

from Engine.Keyframe.Transform import *


class TextElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D,
                 axes, s_text: str, s_size, **kwargs):
        AnimationElement.__init__(self, start, duration, position)

        self._axes = axes
        self._textArgs = kwargs
        self._text = s_text
        self._size = s_size

    def _instantiate(self):
        self._textElem = self._axes.text(self._position.x, self._position.y, self._text,
                                         self._textArgs, fontsize=self._size)

        self._keyframeMng.attach_handle(self._textElem)

    def _update(self, p):
        self._keyframeMng.update(p)

    def _cleanup(self):
        self._textElem.set_visible(False)
        return 0
