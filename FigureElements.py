from AnimationElement import AnimationElement
from myMaths import Vec2D
from Transform import *

class AxesData:
    def __init__(self, **kwargs):
        self.xlim = [-1, 1]
        self.ylim = [-1, 1]

class AxesStyling:
    def __init__(self, **kwargs):
        self.facecolor = 


class AxesElement(AnimationElement):
    def __init__(self, start: float, duration: float, position: Vec2D, size: Vec2D,
                 main_fig, label, projection):
        super().__init__(start, duration, position)
        self._size = size
        self._main_fig = main_fig
        self.label = label
        self.projection = projection

    def _inset(self):
        self._axes = self._main_fig.add_axes([self._position.x, self._position.y, self._size.x, self._size.y],
                                             label=self.label, anchor='C', projection=self.projection)

    def _style(self):
        self._axes.patch.set_alpha(0)
        self._axes.spines["top"].set_color('white')
        self._axes.spines["bottom"].set_color('white')
        self._axes.spines["left"].set_color('white')
        self._axes.spines["right"].set_color('white')
        self._axes.tick_params(axis='x', colors='white')
        self._axes.set_xlabel("x-label", color="white")
        self._axes.tick_params(axis='y', colors='white')
        self._axes.set_xlabel("y-label", color="white")

    def _instantiate(self):
        self._inset()
        self._style()
        self._keyframeMng.attach_handle(self._axes)
        try:
            return self._init()
        except Exception as detail:
            print("Error:", detail)
        return 0

    def _init(self):
        raise Exception("Figure Init Not Implemented")

    def _update(self, p):
        self._keyframeMng.update(p)
        try:
            return self._refresh(p)
        except Exception as detail:
            print("Error:", detail)
        return 0

    def _refresh(self, p):
        raise Exception("Figure Refresh Not Implemented")

    def _cleanup(self):
        self._axes.remove()
        return 0
