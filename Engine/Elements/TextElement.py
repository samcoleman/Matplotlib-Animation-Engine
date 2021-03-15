from matplotlib.text import Text

from Engine.Elements.AnimationElement import AnimationElement
from Engine.MathsHelpers import Vec2D
from typing import Union


class TextElement(AnimationElement):
    def __init__(self, position: Vec2D, s_text: str, s_size: float, **kwargs) -> None:
        AnimationElement.__init__(self, position)

        self._textElem: Union[None, Text] = None
        self._textArgs = kwargs
        self._text = s_text
        self._size = s_size

    def _instantiate(self) -> None:
        self._textElem = self._main_axes.text(self._position.x, self._position.y, self._text,
                                              self._textArgs, fontsize=self._size)

    def _get_handle(self) -> Text:
        return self._textElem

    def _update(self, progress: float, duration: float):
        return

    def _cleanup(self) -> None:
        self._textElem.set_visible(False)
        return
