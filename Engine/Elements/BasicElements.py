from Engine.Elements.AnimationElement import AnimationElement
from Engine.MathsHelpers import Vec2D


class TextElement(AnimationElement):
    def __init__(self, position: Vec2D, s_text: str, s_size, **kwargs):
        AnimationElement.__init__(self, position)

        self._textElem = None
        self._textArgs = kwargs
        self._text = s_text
        self._size = s_size

    def _instantiate(self):
        self._textElem = self._main_axes.text(self._position.x, self._position.y, self._text,
                                              self._textArgs, fontsize=self._size)

    def get_text(self):
        return self._textElem

    def _update(self, progress: float, duration: float):
        return

    def _cleanup(self):
        self._textElem.set_visible(False)
        return
